# 📄 Guide de Fichier : `engine/vlsm_solver.py`

Le fichier [`engine/vlsm_solver.py`](file:///c:/Users/lenovo/Desktop/laformatik/ipv4-subnet-toolkit/v1.2.0/engine/vlsm_solver.py) implémente l'algorithme de découpage à masque variable **VLSM (Variable Length Subnet Mask)** et intègre les exercices officiels du cours de réseaux de l'INPT.

---

## 1. Rôle dans l'Architecture

Le découpage traditionnel en sous-réseaux à masque fixe (FLSM - Fixed Length Subnet Mask) impose la même taille de bloc à tous les sous-réseaux, provoquant un gaspillage massif d'adresses (par exemple attribuer un bloc de 256 adresses à une liaison point-à-point routeur-routeur qui n'en utilise que 2).

Le module `vlsm_solver.py` résout ce problème en implémentant l'**Algorithme Glouton Décroissant VLSM** :
1. Calcul de la plus petite puissance de 2 couvrant les besoins réels ($2^h - 2 \ge N$).
2. Tri strict des demandes par ordre décroissant pour éviter le chevauchement d'adresses.
3. Allocation contiguë des plages d'adresses avec ajustement dynamique des masques `/CIDR`.

---

## 2. Bibliothèques et Modules Importés

```python
from dataclasses import dataclass
import ipaddress
import math
import random
from typing import List
```

### `math.ceil` et `math.log2` (Bibliothèque Standard Python)
- Utilisés pour déterminer le nombre de bits d'hôtes $h$ sans itération manuelle :
  $$h = \lceil \log_2(N + 2) \rceil$$
  où $N$ est le nombre de machines requises et $+2$ réserve l'adresse réseau et l'adresse de diffusion (broadcast).

### `ipaddress.IPv4Network`
- Utilisé pour instancier des réseaux IPv4 avec la directive `strict=False` (permettant de créer un objet réseau même si l'IP fournie n'est pas encore alignée sur le masque).
- Fournit directement `netmask`, `network_address` et `broadcast_address`.

---

## 3. Modèles de Données (DTOs)

### 3.1. `@dataclass(frozen=True) class VlsmAllocation`
Représente une ligne de sous-réseau allouée :
- `rank: int` : Numéro d'ordre (1, 2, 3...) après tri décroissant.
- `hosts_needed: int` : Nombre d'hôtes demandés ($N$).
- `host_bits: int` : Nombre de bits d'hôtes alloués ($h$).
- `cidr: int` : Longueur du préfixe ($32 - h$).
- `block_size: int` : Nombre total d'adresses dans le bloc ($2^h$).
- `usable_capacity: int` : Nombre d'adresses machines utilisables ($2^h - 2$).
- `mask_str`, `network_str`, `first_host_str`, `last_host_str`, `broadcast_str` : Adresses calculées.
- **Propriété `last_octet_summary`** :
  ```python
  @property
  def last_octet_summary(self) -> str:
      fh_last = self.first_host_str.split(".")[-1]
      lh_last = self.last_host_str.split(".")[-1]
      bc_last = self.broadcast_str.split(".")[-1]
      mk_last = self.mask_str.split(".")[-1]
      return f"Plage: .{fh_last} → .{lh_last}  |  Bcast: .{bc_last}  |  Masque: .{mk_last}"
  ```
  Permet à l'Atelier VLSM (Onglet 3) d'auto-compléter instantanément le résumé synthétique dès que l'étudiant a trouvé le bon CIDR et la bonne adresse réseau.

### 3.2. `@dataclass(frozen=True) class VlsmProblem`
Représente un exercice complet :
- `title: str` : Titre de l'exercice (ex: `"📘 Ex. Cours 1 (193.225.34.0/24 — 44, 20, 100)"`).
- `base_network_str: str` : Adresse réseau de départ (ex: `"193.225.34.0"`).
- `base_cidr: int` : Préfixe de base (ex: `24`).
- `unsorted_needs: List[int]` : Besoins bruts non triés (ex: `[44, 20, 100]`), forçant l'élève à appliquer la règle de tri.
- `allocations: List[VlsmAllocation]` : Solution ordonnée.

---

## 4. Analyse des Méthodes de `VlsmSolver`

### 4.1. `smallest_host_bits(hosts_needed: int) -> int`
```python
@staticmethod
def smallest_host_bits(hosts_needed: int) -> int:
    if hosts_needed < 1:
        return 2
    h = max(2, math.ceil(math.log2(hosts_needed + 2)))
    while (1 << h) - 2 < hosts_needed:
        h += 1
    return h
```
- **Règle Réseau INPT** : Pour accueillir $N$ machines, il faut satisfaire l'inégalité fondamentale :
  $$2^h - 2 \ge N$$
  où $h$ est le nombre de bits réservés à la partie hôte.
- Le minimum absolu pour un sous-réseau standard est $h = 2$ ($2^2 - 2 = 2$ hôtes utilisables pour un masque `/30`).
- La boucle `while` offre une sécurité numérique contre les imprécisions d'arrondi en virgule flottante de `math.log2`.

### 4.2. `solve(base_network_str, base_cidr, needs, title) -> VlsmProblem`
C'est le moteur de résolution séquentiel :
1. **Tri Décroissant Impératif** :
   ```python
   sorted_needs = sorted(needs, reverse=True)
   ```
   *Pourquoi est-ce capital ?* Allouer d'abord les petits sous-réseaux (ex: un bloc de 8 adresses) morcellerait l'espace d'adressage et empêcherait d'aligner un futur grand bloc (ex: 128 adresses) sur une frontière d'adresse multiple de 128.
2. **Boucle d'Allocation Séquentielle** :
   - Pour chaque besoin $N_i$ dans la liste triée :
     - Détermine $h_i$ via `smallest_host_bits(N_i)`.
     - $\text{CIDR}_i = 32 - h_i$.
     - $\text{Taille du bloc}_i = 2^{h_i}$.
     - Le sous-réseau démarre à `current_ip_int`.
     - L'adresse réseau suivante commence immédiatement à $\text{current\_ip\_int} + \text{Taille du bloc}_i$.

### 4.3. Presets Officiels du Cours INPT
- **`preset_cours_1()`** :
  - Réseau de base : `193.225.34.0/24`.
  - Besoins non triés : `[44, 20, 100]`.
  - Résolution :
    1. 100 hôtes $\implies h=7$, masque `/25` (`.128`), bloc de 128 $\implies$ `193.225.34.0/25` (hôtes `.1` à `.126`, broadcast `.127`).
    2. 44 hôtes $\implies h=6$, masque `/26` (`.192`), bloc de 64 $\implies$ `193.225.34.128/26` (hôtes `.129` à `.190`, broadcast `.191`).
    3. 20 hôtes $\implies h=5$, masque `/27` (`.224`), bloc de 32 $\implies$ `193.225.34.192/27` (hôtes `.193` à `.222`, broadcast `.223`).
- **`preset_cours_2()`** :
  - Réseau de base : `192.168.0.0/24`.
  - Besoins non triés : `[28, 4, 100]`.
  - Résolution : 100 hôtes (`/25`), 28 hôtes (`/27`), 4 hôtes (`/29`).

### 4.4. `generate_random_problem() -> VlsmProblem`
- Génère dynamiquement un exercice VLSM aléatoire en choisissant parmi des triplets valides d'exposants $(h_1, h_2, h_3)$ dont la somme des blocs ne dépasse jamais la capacité d'un réseau `/24` ($2^{h_1} + 2^{h_2} + 2^{h_3} \le 256$, ex: $(7, 6, 5) \implies 128 + 64 + 32 = 224 \le 256$).
- Mélange délibérément les besoins avant de les présenter à l'élève pour évaluer sa capacité à les trier.
