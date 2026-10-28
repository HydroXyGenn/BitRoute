# 📄 Guide de Fichier : `engine/drills_solver.py`

Le fichier [`engine/drills_solver.py`](file:///c:/Users/lenovo/Desktop/laformatik/ipv4-subnet-toolkit/v1.2.0/engine/drills_solver.py) implémente les générateurs et résolveurs des trois mini-exercices du cours de réseaux INPT intégrés dans l'**Onglet 4 (Flash Drills)** :
1. **📦 Fragmentation IPv4 / MTU** (IHL, multiples de 8 octets, champ Offset, drapeau MF).
2. **🧭 Routage IP & Longest Prefix Match** (LPM, Distance Administrative, Métrique, Route par défaut).
3. **🧮 Checksum d'En-tête IPv4 16 bits** (Addition hexadécimale, report de retenue *End-Around Carry*, complément à un).

---

## 1. Bibliothèques et Modules Importés

```python
from dataclasses import dataclass
import ipaddress
import random
from typing import List, Tuple
```

- **`dataclasses`** : Structures immuables représentant un fragment IP (`MtuFragment`), un problème de MTU (`MtuProblem`), une ligne de table de routage (`RouteEntry`), une décision LPM (`LpmProblem`), et un calcul de checksum (`ChecksumProblem`).
- **`ipaddress`** : Utilisé dans `ip_matches_prefix()` pour tester si l'IP de destination appartient au réseau d'une route via l'opérateur d'appartenance `ip_obj in net_obj`.
- **`random`** : Utilisé pour générer des adresses de destination et des scénarios de décision variés.

---

## 2. Section 1 : Fragmentation MTU IPv4

### 2.1. Principes Théoriques Réseau (RFC 791)
Lorsqu'un paquet IPv4 traverse un lien dont la **MTU (Maximum Transmission Unit)** est inférieure à sa taille totale, le routeur doit le scinder en plusieurs fragments :
1. **Longueur de l'en-tête IP** :
   $$\text{Header Length} = \text{IHL} \times 4 \text{ octets}$$
   Pour la valeur standard $\text{IHL} = 5$, l'en-tête mesure $5 \times 4 = 20 \text{ octets}$.
2. **Charge Utile Maximale par Fragment (Règle du Multiple de 8)** :
   $$\text{Max Payload} = \left\lfloor \frac{\text{MTU} - \text{Header Length}}{8} \right\rfloor \times 8$$
   *Pourquoi un multiple de 8 ?* Le champ *Fragment Offset* de l'en-tête IPv4 ne dispose que de 13 bits pour exprimer une position dans un paquet pouvant mesurer jusqu'à 65 535 octets. Il compte donc la position en **unités de 8 octets** ($2^{16} / 2^3 = 2^{13}$).
3. **Champ Déplacement (Fragment Offset)** :
   $$\text{Offset Field} = \frac{\text{Octet de début}}{8}$$
4. **Drapeau MF (More Fragments)** :
   - `MF = 1` si d'autres fragments suivent.
   - `MF = 0` pour le dernier fragment de la séquence.

### 2.2. Algorithme de `solve_mtu()`
```python
@staticmethod
def solve_mtu(total_length: int, ihl: int, mtu: int, title: str) -> MtuProblem:
    header_len = ihl * 4
    orig_data = max(0, total_length - header_len)
    max_data = ((mtu - header_len) // 8) * 8

    fragments: List[MtuFragment] = []
    remaining = orig_data
    byte_pos = 0
    idx = 1

    while remaining > 0:
        payload = min(max_data, remaining)
        remaining -= payload
        mf = 1 if remaining > 0 else 0
        offset = byte_pos // 8
        fragments.append(MtuFragment(idx, payload + header_len, payload, offset, mf))
        byte_pos += payload
        idx += 1
```

### 2.3. Cas Pratique Officiel du Cours INPT (`preset_mtu_cours`)
- **Données** : Longueur totale = 4000 octets, $\text{IHL} = 5$ (en-tête 20 octets), $\text{MTU} = 1500$.
- **Données à fragmenter** : $4000 - 20 = 3980 \text{ octets}$.
- **Charge utile max par fragment** : $\lfloor (1500 - 20) / 8 \rfloor \times 8 = \lfloor 1480 / 8 \rfloor \times 8 = 1480 \text{ octets}$.
- **Décomposition** :
  - **Fragment 1** : 1480 octets de données, $\text{Offset} = 0 / 8 = 0$, $\text{MF} = 1$.
  - **Fragment 2** : 1480 octets de données, $\text{Offset} = 1480 / 8 = 185$, $\text{MF} = 1$.
  - **Fragment 3** : Reste $3980 - (2 \times 1480) = 1020 \text{ octets}$, $\text{Offset} = 2960 / 8 = 370$, $\text{MF} = 0$.

---

## 3. Section 2 : Décision de Routage & LPM

### 3.1. Hiérarchie de Décision d'un Routeur IP
Face à un paquet à router vers une adresse IP destination, un routeur applique les critères d'évaluation dans un **ordre de priorité strict et non négociable** :

```
             ┌──────────────────────────────────────────────┐
             │ 1. Plus Long Préfixe Correspondant (LPM)     │
             │    Le masque le plus spécifique l'emporte    │
             └──────────────────────┬───────────────────────┘
                                    │ Égalité de masque ?
                                    ▼
             ┌──────────────────────────────────────────────┐
             │ 2. Plus Petite Distance Administrative (AD)  │
             │    Connecté (0) > Stat. (1) > OSPF (110) ... │
             └──────────────────────┬───────────────────────┘
                                    │ Même protocole (même AD) ?
                                    ▼
             ┌──────────────────────────────────────────────┐
             │ 3. Plus Faible Métrique                      │
             │    Coût / Bande passante / Hop count         │
             └──────────────────────┬───────────────────────┘
                                    │ Aucune route spécifique ?
                                    ▼
             ┌──────────────────────────────────────────────┐
             │ 4. Route par Défaut (0.0.0.0/0)              │
             │    Passerelle de dernier recours             │
             └──────────────────────────────────────────────┘
```

### 3.2. Méthode `generate_lpm_problem(scenario)`
Génère 4 scénarios d'évaluation didactiques :
1. **Scénario `lpm`** : Compare une route `/25` avec protocole RIP ($\text{AD} = 120$) contre une route `/24` statique ($\text{AD} = 1$). *Le piège classique* : les étudiants pensent que la route statique gagne car $\text{AD}=1 < 120$. En réalité, le critère LPM prime : `/25` l'emporte immédiatement sur `/24`.
2. **Scénario `ad`** : Deux routes ont le même préfixe `/24`, l'une apprise par OSPF ($\text{AD} = 110$), l'autre par RIP ($\text{AD} = 120$). OSPF gagne grâce à sa distance administrative plus fiable.
3. **Scénario `metric`** : Deux routes OSPF partagent le même préfixe `/24` et la même distance ($\text{AD} = 110$). Le routeur choisit celle ayant le coût le plus faible (métrique $20 < 65$).
4. **Scénario `default`** : L'adresse publique de destination ne correspond à aucun réseau d'entreprise de la table. Le routeur utilise `0.0.0.0/0` (`S*`).

---

## 4. Section 3 : Checksum d'En-tête IPv4 16 bits

### 4.1. Principe Mathématique (RFC 791 / RFC 1071)
Le champ Checksum de l'en-tête IPv4 protège contre la corruption physique des paquets :
1. **Initialisation** : Le champ checksum de l'en-tête est mis à `0x0000`.
2. **Addition Brute** : On somme tous les mots de 16 bits de l'en-tête (5 à 15 mots selon IHL).
3. **End-Around Carry (Rabattement de Retenue)** :
   - En arithmétique complément à un sur 16 bits, tout dépassement au-delà de 16 bits (les bits $16$ à $31$) représente une retenue qui doit être **réinjectée en l'additionnant au bit de poids faible** (à droite).
   - En code :
     ```python
     while carried > 0xFFFF:
         carried = (carried & 0xFFFF) + (carried >> 16)
     ```
4. **Complément à un Final** :
   $$\text{Checksum} = (\sim\text{carried}) \ \& \ \text{0xFFFF}$$

### 4.2. Exemple Officiel du Cours INPT (`preset_checksum_cours`)
- **10 mots hexadécimaux de l'en-tête** :
  `4500`, `0054`, `0000`, `4000`, `4001`, `0000`, `C0A8`, `0068`, `C0A8`, `0001`.
- **Étape 1 : Somme brute** :
  $$\text{Somme} = \text{0x2470E}$$
- **Étape 2 : Rabattement de retenue** :
  - Bits 0 à 15 = `0x470E`
  - Retenue (bits décalés de 16) = `0x2`
  - Somme rabattue = $\text{0x470E} + \text{0x2} = \text{0x4710}$
- **Étape 3 : Complément à un final** :
  $$\sim\text{0x4710} \ \& \ \text{0xFFFF} = \text{0xB8EF}$$

### 4.3. `parse_hex_input(text: str) -> int`
Méthode utilitaire qui convertit la chaîne saisie par l'étudiant en entier, en tolérant les préfixes `"0x"`, `"0X"`, les espaces et les majuscules/minuscules, tout en retournant `-1` si la chaîne est invalide.
