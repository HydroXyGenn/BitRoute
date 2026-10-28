# 02 — Algorithmes du Cours INPT & Exercices Résolus (`vlsm_solver.py` & `drills_solver.py`)

Ce document détaille tous les algorithmes réseau du cours **INPT ASEDS** implémentés dans `engine/vlsm_solver.py` et `engine/drills_solver.py`, avec leurs démonstrations mathématiques et les exemples officiels du cours.

---

## 1. Algorithme de Découpage VLSM (`engine/vlsm_solver.py`)

### 1.1. Pourquoi trier par ordre strictement décroissant ?
En VLSM (*Variable Length Subnet Mask*), un bloc de taille $2^h$ doit obligatoirement commencer à une adresse IP qui est un **multiple entier de $2^h$** (alignement binaire des frontières de sous-réseau).
- Si l'on alloue d'abord les grands blocs ($2^{h_1} \ge 2^{h_2} \ge 2^{h_3}$), chaque sous-réseau suivant démarre naturellement sur un multiple de sa propre taille $2^{h_i}$, sans aucun trou ni chevauchement !
- À l'inverse, si l'on allouait d'abord un petit bloc `/27` (taille 32, de `.0` à `.31`), le bloc `/25` suivant (taille 128) ne pourrait pas commencer à `.32` (car `32 & 128 != 0`) et devrait sauter à `.128`, créant une fragmentation de l'espace d'adressage.

### 1.2. Formule de dimensionnement d'un sous-réseau
Pour un besoin de $N$ machines hôtes :
1. On cherche le plus petit entier $h \ge 2$ tel que :
   $$2^h - 2 \ge N \iff 2^h \ge N + 2$$
   *(Les 2 adresses soustraites correspondent à l'adresse Réseau — tous les bits hôtes à `0` — et à l'adresse de Diffusion/Broadcast — tous les bits hôtes à `1`).*
   En Python : `h = max(2, math.ceil(math.log2(N + 2)))`.
2. Le nouveau préfixe CIDR vaut :
   $$\text{CIDR} = 32 - h$$
3. Le pas (taille du bloc) vaut :
   $$\text{BlockSize} = 2^h$$
4. Si le sous-réseau courant commence à l'entier 32 bits $A_{\text{net}}$ :
   - $\text{Network} = A_{\text{net}}$
   - $\text{First Host} = A_{\text{net}} + 1$
   - $\text{Last Host} = A_{\text{net}} + 2^h - 2$
   - $\text{Broadcast} = A_{\text{net}} + 2^h - 1$
   - $\text{Next Base} = A_{\text{net}} + 2^h$

### 1.3. Vérification sur les 2 Presets Officiels du Cours
* **Preset Cours 1** : Réseau `193.225.34.0/24`, besoins `[44, 20, 100]`
  1. Tri décroissant : `100`, puis `44`, puis `20`.
  2. **SR #1 (100 hôtes)** : $2^7 - 2 = 126 \ge 100 \implies h=7 \implies /25$ (`255.255.255.128`), bloc de $128$ :
     - Réseau : `193.225.34.0/25` | Hôtes : `.1` à `.126` | Broadcast : `.127`.
  3. **SR #2 (44 hôtes)** : $2^6 - 2 = 62 \ge 44 \implies h=6 \implies /26$ (`255.255.255.192`), bloc de $64$ :
     - Réseau : `193.225.34.128/26` | Hôtes : `.129` à `.190` | Broadcast : `.191`.
  4. **SR #3 (20 hôtes)** : $2^5 - 2 = 30 \ge 20 \implies h=5 \implies /27$ (`255.255.255.224`), bloc de $32$ :
     - Réseau : `193.225.34.192/27` | Hôtes : `.193` à `.222` | Broadcast : `.223`.

* **Preset Cours 2** : Réseau `192.168.0.0/24`, besoins `[100, 28, 4]`
  1. **SR #1 (100 hôtes)** : $h=7 \implies /25$ (bloc 128) $\rightarrow$ `192.168.0.0/25`, plage `.1` à `.126`, Broadcast `.127`.
  2. **SR #2 (28 hôtes)** : $2^5 - 2 = 30 \ge 28 \implies h=5 \implies /27$ (bloc 32) $\rightarrow$ `192.168.0.128/27`, plage `.129` à `.158`, Broadcast `.159`.
  3. **SR #3 (4 hôtes)** : $2^3 - 2 = 6 \ge 4 \implies h=3 \implies /29$ (bloc 8) $\rightarrow$ `192.168.0.160/29`, plage `.161` à `.166`, Broadcast `.167`.

---

## 2. Fragmentation IPv4 & MTU (`engine/drills_solver.py`)

### 2.1. Formules fondamentales
- **Taille de l'en-tête IPv4** : Le champ `IHL` (*Internet Header Length*, sur 4 bits) exprime la longueur de l'en-tête en **mots de 32 bits (4 octets)** :
  $$L_{\text{header}} = \text{IHL} \times 4 \text{ octets}$$
  Pour un en-tête standard sans options ($\text{IHL} = 5$), $L_{\text{header}} = 20\text{ octets}$.
- **Données utiles initiales (Payload original)** :
  $$D_{\text{total}} = \text{Total Length} - L_{\text{header}}$$
- **Données max par fragment (Alignement sur 8 octets)** :
  Le champ `Fragment Offset` dans l'en-tête IPv4 fait 13 bits alors que `Total Length` fait 16 bits ($2^{16} / 2^{13} = 2^3 = 8$). L'unité d'offset est donc un **bloc de 8 octets**. Par conséquent, chaque fragment (sauf éventuellement le dernier) doit transporter un nombre d'octets de données **multiple de 8** :
  $$D_{\max} = \left\lfloor \frac{\text{MTU} - L_{\text{header}}}{8} \right\rfloor \times 8$$
- **Calcul itératif des fragments** :
  Pour chaque fragment $i$ commençant à l'octet de données `byte_pos` :
  - $\text{Payload}_i = \min(D_{\max}, \text{restant})$
  - $\text{Offset}_i = \text{byte\_pos} / 8$
  - $\text{MF}_i = 1$ s'il reste des données après ce fragment, sinon $0$.

### 2.2. Exemple officiel du cours (`Total = 4000`, `IHL = 5`, `MTU = 1500`)
- $L_{\text{header}} = 5 \times 4 = 20\text{ octets}$.
- $D_{\text{total}} = 4000 - 20 = 3980\text{ octets}$.
- $D_{\max} = \lfloor (1500 - 20) / 8 \rfloor \times 8 = \lfloor 1480 / 8 \rfloor \times 8 = 185 \times 8 = 1480\text{ octets}$.
- **Fragment #1** : `1480` octets de données (octets `0` à `1479`), $\text{Offset} = 0 / 8 = 0$, $\text{MF} = 1$.
- **Fragment #2** : `1480` octets de données (octets `1480` à `2959`), $\text{Offset} = 1480 / 8 = 185$, $\text{MF} = 1$.
- **Fragment #3** : $3980 - 2960 = 1020$ octets de données (octets `2960` à `3979`), $\text{Offset} = 2960 / 8 = 370$, $\text{MF} = 0$.

---

## 3. Routage IPv4 & Hiérarchie de Décision (`engine/drills_solver.py`)

Lorsqu'un routeur reçoit un paquet destiné à `IP_dest`, il applique **strictement dans cet ordre** :
1. **Filtrage d'appartenance** : Ne conserver que les entrées `Réseau/CIDR` telles que `IP_dest in Réseau/CIDR`. (Piège classique : une route en `/26` dans la table a un masque long, mais si `IP_dest` est en `.80` alors que le `/26` couvre `.0` à `.63`, cette route est éliminée dès l'étape 1 !).
2. **Règle 1 — Longest Prefix Match (LPM)** : Parmi les routes correspondantes, choisir celle ayant le `/CIDR` le plus grand (`/25 > /24 > /16 > /0`), peu importe le protocole ou la métrique.
3. **Règle 2 — Distance Administrative (AD)** : En cas d'égalité de `/CIDR`, choisir la source la plus fiable (plus petite AD) :
   - Connecté (`C`) = `0`
   - Statique (`S`) = `1`
   - OSPF (`O`) = `110`
   - RIP (`R`) = `120`
4. **Règle 3 — Métrique** : En cas d'égalité de `/CIDR` et d'AD (même protocole), choisir la plus petite métrique (coût OSPF ou nombre de sauts RIP).
5. **Route par défaut (`0.0.0.0/0`, `S*`)** : Correspond à toutes les IP avec un préfixe `/0` (le plus court possible) ; elle n'est choisie que si aucune autre route plus spécifique ne correspond.

---

## 4. Checksum de l'En-tête IPv4 sur 16 bits (`engine/drills_solver.py`)

### 4.1. Algorithme de somme en complément à un (RFC 791 / RFC 1071)
1. Découper l'en-tête IPv4 (20 octets si `IHL=5`) en **10 mots de 16 bits** hexadécimaux, en forçant le 6ème mot (champ Checksum) à `0x0000`.
2. Calculer la **somme brute** :
   $$S_{\text{raw}} = \sum_{k=1}^{10} W_k$$
3. **Rabattement des retenues (End-Around Carry)** : Tant que la somme dépasse 16 bits ($S > \text{0xFFFF}$), ajouter les bits de poids fort aux 16 bits de poids faible :
   ```python
   carried = raw_sum
   while carried > 0xFFFF:
       carried = (carried & 0xFFFF) + (carried >> 16)
   ```
4. **Complément à un final** : Inverser les 16 bits :
   $$\text{Checksum} = (\sim S_{\text{carried}}) \ \& \ \text{0xFFFF} = \text{0xFFFF} - S_{\text{carried}}$$

### 4.2. Exemple officiel du cours
Mots de 16 bits : `4500 0054 0000 4000 4001 0000 C0A8 0068 C0A8 0001`
- **Étape 1 (Somme brute)** :
  $$\text{0x4500} + \text{0x0054} + \text{0x0000} + \text{0x4000} + \text{0x4001} + \text{0x0000} + \text{0xC0A8} + \text{0x0068} + \text{0xC0A8} + \text{0x0001} = \text{0x2470E}$$
- **Étape 2 (End-Around Carry)** :
  $$\text{0x470E} + \text{0x0002} = \text{0x4710}$$
- **Étape 3 (Complément à un)** :
  $$\sim\text{0x4710} \ \& \ \text{0xFFFF} = \text{0xFFFF} - \text{0x4710} = \text{0xB8EF}$$
