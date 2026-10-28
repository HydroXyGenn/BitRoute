# 01 — Architecture du Moteur (`engine/`) & Mathématiques Réseau

Ce document rassemble les concepts d'architecture logicielle et de mathématiques réseau implémentés dans la **Phase 1 (`engine/`)** de **IPv4 Subnet Toolkit v1.2.0**, afin de préparer le guide PDF final.

---

## 1. Découplage Moteur / Interface (Clean Architecture & Java Porting)

### Pourquoi séparer `engine/` et `ui/` ?
Dans la version `v1.0.0`, toute la logique (calculs `ipaddress`, manipulation binaire, validation des saisies, génération aléatoire) était imbriquée directement dans les méthodes des classes `QWidget` (`BinaryConverterTab`, `SubnetPracticeTab`).

En `v1.2.0`, nous appliquons le principe de **Séparation des Préoccupations (Separation of Concerns - SoC)** :
1. **Zéro dépendance GUI dans `engine/`** : Aucun fichier de `engine/` n'importe `PyQt6`. Le moteur ne manipule que des types primitifs (`int`, `str`, `bool`, `list`) et des objets de données immuables (`@dataclass(frozen=True)`).
2. **Testabilité immédiate** : On peut tester 100 % des cas du cours INPT en ligne de commande en quelques millisecondes sans lancer de fenêtre graphique.
3. **Portabilité directe vers Java (Cursus ASEDS INPT)** :
   - Chaque `@dataclass(frozen=True)` Python (`OctetAnalysis`, `SubnetAnalysis`, `VlsmAllocation`, `MtuFragment`, `RouteEntry`, `ChecksumProblem`) correspond directement à un `record` Java (Java 16+) ou une classe POJO finale avec attributs `private final` et getters.
   - Chaque classe de service (`IPv4MathEngine`, `VlsmSolver`, `DrillsSolver`) regroupe des méthodes statiques/pures faciles à traduire en méthodes `public static` en Java.

---

## 2. Bitwise Math & Manipulation d'Octets (`engine/ipv4_math.py`)

### 2.1. Contiguïté des bits d'un octet de masque
Un masque de sous-réseau IPv4 valide est constitué d'une suite ininterrompue de `1` (partie réseau) suivie d'une suite ininterrompue de `0` (partie hôte).
Sur un seul octet (8 bits), il n'existe donc que **9 valeurs décimales valides** :
- `00000000` = `0`
- `10000000` = `128`
- `11000000` = `192`
- `11100000` = `224`
- `11110000` = `240`
- `11111000` = `248`
- `11111100` = `252`
- `11111110` = `254`
- `11111111` = `255`

### 2.2. Complément à un sur 8 bits et 32 bits en Python
En Python, les entiers (`int`) ont une précision arbitraire (signés). L'opérateur binaire `~x` calcule `-x - 1` (complément à deux signé).
Pour obtenir le **complément à un non signé** :
- Sur **8 bits** (un octet) : `(~val) & 0xFF` (équivalent arithmétique : `255 - val`).
- Sur **32 bits** (adresse IPv4 complète / Wildcard Mask) : `(~mask_int) & 0xFFFFFFFF`.

### 2.3. Le "Magic Number" (Pas du sous-réseau)
Pour un octet de masque $M$, la taille du bloc (le pas entre deux sous-réseaux consécutifs dans cet octet) vaut :
$$\text{Pas} = 256 - M$$
*Exemple* : Si le masque est `255.255.255.192` (`/26`), le pas dans le 4ème octet est $256 - 192 = 64$. Les sous-réseaux commencent donc à `.0`, `.64`, `.128`, `.192`.

### 2.4. Opérations 32 bits : Réseau, Host ID Interne et Broadcast
En convertissant l'IP et le masque en entiers 32 bits (`0` à `4294967295`) :
- **Masque 32 bits depuis `/CIDR`** :
  $$\text{Mask} = (\text{0xFFFFFFFF} \ll (32 - \text{CIDR})) \ \& \ \text{0xFFFFFFFF}$$
- **Adresse Réseau** :
  $$\text{Network} = \text{IP} \ \& \ \text{Mask}$$
- **Host ID Interne** (identifiant de la machine à l'intérieur de son sous-réseau) :
  $$\text{HostID} = \text{IP} \ \& \ (\sim\text{Mask} \ \& \ \text{0xFFFFFFFF})$$
- **Adresse de Diffusion (Broadcast)** :
  $$\text{Broadcast} = \text{Network} \mid (\sim\text{Mask} \ \& \ \text{0xFFFFFFFF})$$

### 2.5. Bits empruntés ($b_S$) et Bits d'hôtes ($b_H$)
Par rapport au masque par défaut de la classe (`Classe A = /8`, `Classe B = /16`, `Classe C = /24`) :
- $b_S = \text{CIDR} - \text{CIDR}_{\text{défaut}} \implies 2^{b_S}$ sous-réseaux créés.
- $b_H = 32 - \text{CIDR} \implies 2^{b_H} - 2$ hôtes utilisables par sous-réseau.
- *Cas de vérification du cours* : `154.4.32.0/19` est de **Classe B** ($128 \le 154 \le 191$, défaut `/16`). On emprunte $b_S = 19 - 16 = 3$ bits ($2^3 = 8$ sous-réseaux) et il reste $b_H = 32 - 19 = 13$ bits d'hôtes ($2^{13} - 2 = 8190$ machines).
