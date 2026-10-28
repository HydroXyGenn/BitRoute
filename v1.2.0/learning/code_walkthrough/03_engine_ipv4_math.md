# 📄 Guide de Fichier : `engine/ipv4_math.py`

Le fichier [`engine/ipv4_math.py`](file:///c:/Users/lenovo/Desktop/laformatik/ipv4-subnet-toolkit/v1.2.0/engine/ipv4_math.py) constitue le **cœur arithmétique et logique** de l'application. Il prend en charge l'intégralité des calculs binaires, l'inspection de validité des octets de masque, la classification historique par classe (RFC 791), la détection des portées privées (RFC 1918) et le découpage binaire sur 32 bits.

Il ne possède **aucune dépendance vers PyQt6**, garantissant une exécution purement algorithmique.

---

## 1. Bibliothèques et Modules Importés

```python
from dataclasses import dataclass
import ipaddress
import random
from typing import Dict, Optional, Tuple
```

### `dataclasses.dataclass` (avec `frozen=True`)
- Utilisé pour définir des structures de données de transfert (DTO) rigides et immuables.
- Le paramètre `frozen=True` rend les instances en lecture seule après leur instanciation. Tenter de modifier un attribut (par exemple `analysis.cidr = 24`) lève une exception `FrozenInstanceError`. Cela garantit qu'un résultat de calcul réseau ne peut jamais être corrompu accidentellement par un composant d'interface.

### `ipaddress` (Bibliothèque Standard Python)
- Fournit l'objet `IPv4Address` pour valider la syntaxe des adresses IP et convertir de manière fiable les entiers 32 bits non signés en notation décimale pointée (`str(IPv4Address(val_32))`).

### `random` (Bibliothèque Standard Python)
- Utilisé dans `generate_practice_problem()` pour générer des exercices variés et équilibrés en couvrant toutes les classes d'adresses et portées du cours.

### `typing` (`Dict`, `Optional`, `Tuple`)
- Permet un typage statique strict (PEP 484) pour toutes les signatures de fonctions, documentant explicitement les types d'arguments et de retours pour les développeurs et l'IDE.

---

## 2. Constantes Globales & Objets de Données (DTOs)

### 2.1. `VALID_MASK_OCTETS`
```python
VALID_MASK_OCTETS: Tuple[int, ...] = (255, 254, 252, 248, 240, 224, 192, 128, 0)
```
- **Règle Réseau INPT** : Dans un masque de sous-réseau IPv4, les bits à `1` doivent être strictement contigus de gauche à droite. Sur un seul octet (8 bits), il n'existe mathématiquement que **9 valeurs possibles** respectant cette règle :
  - `11111111` = 255
  - `11111110` = 254
  - `11111100` = 252
  - `11111000` = 248
  - `11110000` = 240
  - `11100000` = 224
  - `11000000` = 192
  - `10000000` = 128
  - `00000000` = 0
- Toute autre valeur (ex: 160 = `10100000`) présente une alternance de `1` et `0` et est donc **invalide** pour un masque.

### 2.2. `@dataclass(frozen=True) class OctetAnalysis`
Modélise l'inspection d'un octet (0 à 255) pour l'Onglet 1 :
- `value: int` : Valeur décimale.
- `binary_str: str` : Représentation binaire sur 8 caractères (ex: `"11000000"`).
- `hex_str: str` : Représentation hexadécimale (ex: `"0xC0"`).
- `is_valid_mask_octet: bool` : `True` si l'octet fait partie de `VALID_MASK_OCTETS`.
- `ones_complement: int` : Complément à un sur 8 bits ($255 - \text{valeur}$).
- `ones_complement_binary: str` : Binaire du complément à un sur 8 bits.
- `block_size: int` : Pas du sous-réseau / "Magic Number" ($256 - \text{valeur}$).

### 2.3. `@dataclass(frozen=True) class SubnetAnalysis`
Contient l'analyse exhaustive d'une adresse IP et de son préfixe `/CIDR` (Onglet 2) :
- Adresses en notation décimale : `ip_str`, `mask_str`, `wildcard_str`, `network_str`, `broadcast_str`, `first_host_str`, `last_host_str`, `next_subnet_str`, `internal_host_id_str`.
- Classification : `ip_class` (A, B, C, D, E), `default_class_cidr` (/8, /16, /24), `leading_bits_pattern` (`"0..."`, `"10..."`, `"110..."`), `address_type` (`"Publique"`, `"Privée"`, `"APIPA"`, `"Loopback"`).
- Métriques du cours : `borrowed_bits` ($b_S$), `host_bits` ($b_H$), `num_subnets_from_class` ($2^{b_S}$), `usable_hosts` ($2^{b_H} - 2$).
- Chaînes binaires 32 bits formatées avec points : `ip_bin_dotted`, `mask_bin_dotted`, `wildcard_bin_dotted`, `network_bin_dotted`, `host_id_bin_dotted`, `broadcast_bin_dotted`.

---

## 3. Analyse Détaillée des Méthodes de `IPv4MathEngine`

### 3.1. `is_valid_mask_octet(val: int) -> bool`
- **Rôle** : Vérifie si l'entier `val` appartient au tuple `VALID_MASK_OCTETS`.
- **Complexité** : $\mathcal{O}(1)$ grâce à la recherche dans un tuple de 9 éléments.

### 3.2. `ones_complement_octet(val: int) -> int`
```python
@staticmethod
def ones_complement_octet(val: int) -> int:
    return (~val) & 0xFF
```
- **Raisonnement Binaire** : En Python, les entiers ont une précision infinie et sont signés. L'opérateur tilde `~val` calcule $-(\text{val} + 1)$ (complément à deux signé).
- Pour obtenir le **complément à un non signé sur 8 bits**, on applique un masque logique ET avec `0xFF` (`255`).
- *Exemple* : Pour `val = 192` (`11000000_2`), `~192 & 0xFF` donne `63` (`00111111_2`), soit exactement $255 - 192$.

### 3.3. `block_size_octet(val: int) -> int`
```python
@staticmethod
def block_size_octet(val: int) -> int:
    return 256 - max(0, min(255, val))
```
- **Règle Réseau ("Magic Number")** : Le pas entre deux sous-réseaux consécutifs dans l'octet significatif vaut $256 - M$, où $M$ est la valeur décimale du masque.
- Pour $M = 192$, le pas vaut $256 - 192 = 64$. Les sous-réseaux progressent de 64 en 64 (`.0`, `.64`, `.128`, `.192`).

### 3.4. `classify_ipv4(ip_str: str) -> Tuple[str, Optional[int], str]`
- **Rôle** : Détermine la classe historique (A, B, C, D, E) selon le 1er octet (RFC 791) :
  - `0 <= o1 <= 127` : **Classe A** (Masque par défaut `/8`, bits de poids fort `"0..."`).
  - `128 <= o1 <= 191` : **Classe B** (Masque par défaut `/16`, bits de poids fort `"10..."`).
  - `192 <= o1 <= 223` : **Classe C** (Masque par défaut `/24`, bits de poids fort `"110..."`).
  - `224 <= o1 <= 239` : **Classe D** (Multicast, pas de masque par défaut, `"1110..."`).
  - `240 <= o1 <= 255` : **Classe E** (Réservée expérimentale, `"11110..."`).

### 3.5. `get_address_type(ip_str: str) -> str`
- **Rôle** : Identifie la portée de l'adresse selon les standards IETF :
  - **Loopback** : `127.0.0.0/8` (RFC 1122).
  - **APIPA** (Automatic Private IP Addressing) : `169.254.0.0/16` (RFC 3927).
  - **Privée (RFC 1918)** :
    - `10.0.0.0/8` (`10.0.0.0` à `10.255.255.255`)
    - `172.16.0.0/12` (`172.16.0.0` à `172.31.255.255`, vérifié par `16 <= o2 <= 31`)
    - `192.168.0.0/16` (`192.168.0.0` à `192.168.255.255`)
  - **Multicast** : `224.0.0.0` à `239.255.255.255`.
  - **Publique** : Toute autre adresse unicast routable sur Internet.

### 3.6. `int_to_dotted_bin(val_32: int) -> str`
- Formate un entier 32 bits sous la forme `"XXXXXXXX.XXXXXXXX.XXXXXXXX.XXXXXXXX"` en découpant la chaîne binaire par tranches de 8 bits.

### 3.7. `analyze_subnet(ip_str: str, cidr: int) -> SubnetAnalysis`
C'est la méthode maîtresse qui exécute les calculs complets sur 32 bits non signés :

1. **Calcul du Masque 32 bits** :
   $$\text{mask\_int} = (\text{0xFFFFFFFF} \ll (32 - \text{cidr})) \ \& \ \text{0xFFFFFFFF}$$
2. **Wildcard Mask (Masque Générique Inversé)** :
   $$\text{wildcard\_int} = (\sim\text{mask\_int}) \ \& \ \text{0xFFFFFFFF}$$
3. **Adresse Réseau** :
   $$\text{network\_int} = \text{ip\_int} \ \& \ \text{mask\_int}$$
4. **Host ID Interne** (identifiant de la machine au sein du sous-réseau) :
   $$\text{host\_id\_int} = \text{ip\_int} \ \& \ \text{wildcard\_int}$$
5. **Adresse de Diffusion (Broadcast)** :
   $$\text{broadcast\_int} = \text{network\_int} \mid \text{wildcard\_int}$$
6. **Plage d'Hôtes Valides** :
   - Premier hôte = $\text{network\_int} + 1$ (si $\text{cidr} \le 30$)
   - Dernier hôte = $\text{broadcast\_int} - 1$ (si $\text{cidr} \le 30$)
7. **Sous-Réseau Suivant (Next Subnet)** :
   $$\text{next\_subnet\_int} = \text{network\_int} + 2^{32 - \text{cidr}}$$
8. **Bits Empruntés ($b_S$) & Bits d'Hôtes ($b_H$)** :
   - $b_S = \text{cidr} - \text{default\_cidr}$ (nombre de sous-réseaux créés = $2^{b_S}$)
   - $b_H = 32 - \text{cidr}$ (nombre d'adresses utilisables = $2^{b_H} - 2$)

### 3.8. `generate_practice_problem() -> SubnetAnalysis`
- Génère un problème aléatoire équilibré pour l'entraînement :
  - 12 % de chances de tomber sur une adresse Loopback (`127.x.x.x`).
  - 12 % de chances de tomber sur une adresse APIPA (`169.254.x.x`).
  - 34 % de chances de tomber sur une adresse Privée RFC 1918 (Classe A, B ou C).
  - 42 % de chances de tomber sur une adresse Publique unicast (Classe A, B ou C).
- Garantit que le CIDR généré est toujours supérieur ou égal au masque par défaut de sa classe (par exemple, au moins `/16` pour la classe B, évitant le super-netting non enseigné à ce stade).

### 3.9. `normalize_ip_input(raw_text: str) -> str`
- Nettoie les saisies utilisateur imparfaites (ex: `"192 168 1 1"` ou `"192,168,1,1"` ou `"192..168.01.001"`) pour produire une chaîne normalisée `"192.168.1.1"`.
