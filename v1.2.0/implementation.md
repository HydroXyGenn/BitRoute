# SPÉCIFICATION TECHNIQUE MAÎTRE — IPv4 Subnet Toolkit v1.2.0

## 1. Vision du Projet & Règles d'Or (Anti-Saturation)
Tu es chargé de faire évoluer l'application PyQt6 existante (`converter.py`) vers la version 1.2.0[cite: 2].
Cette application sert d'outil d'entraînement personnel évolutif pour le cursus ingénieur ASEDS à l'INPT[cite: 3, 185].

### Règles Ergonomiques Strictes (Zéro Surcharge Cognitive)
1. Tester la décision, automatiser la répétition : Ne demande jamais à l'utilisateur de saisir 15 champs répétitifs. Teste uniquement le cœur mathématique (ex: en VLSM, l'utilisateur saisit le `/CIDR` et le `Network ID`, et l'application auto-complète la plage d'hôtes et le Broadcast dès que c'est juste)[cite: 89, 90, 92, 93].
2. Divulgation Progressive : Les explications binaires détaillées sur 32 bits doivent être placées dans un panneau repliable (`🔍 Voir le détail binaire`), fermé par défaut pour garder l'interface épurée.
3. Conservation de l'ADN visuel : Conserver les deux thèmes QSS signature de `converter.py` (Light Mode moderne et 💻 Hacker Dark noir `#000000` / vert phosphore `#00FF66`) ainsi que la saisie rapide au clavier via `IpLineEdit`[cite: 2].

---

## 2. Architecture Cible Modulaire (Découplage Moteur / UI)
Refactoriser le projet en séparant strictement la logique métier (`engine/`) de l'interface graphique (`ui/`).
Note : Le dossier `engine/` doit être écrit avec des classes et méthodes très propres (sans aucun import `PyQt6`), afin de pouvoir servir de modèle de référence pour un futur portage en Java Orienté Objet[cite: 185].

Structure des fichiers à créer :
- ipv4-subnet-toolkit/
  - converter.py             (Point d'entrée principal : lance QApplication et MainWindow)[cite: 2]
  - run_app.bat              (Lanceur Windows existant : start "" pythonw converter.py)[cite: 1]
  - run_app.vbs              (Lanceur VBS existant)[cite: 1]
  - README.md                (Documentation mise à jour pour la v1.2.0)[cite: 1]
  - SPEC_V1_2_0.md           (Ce fichier de spécification)
  - engine/                  (Logique réseau pure : 100% Python standard, ZÉRO PyQt6)
    - __init__.py
    - ipv4_math.py           (Calculs d'octet, masque, classes A-E, types RFC1918, binaire 32 bits)
    - vlsm_solver.py         (Algorithme de découpage VLSM et exercices officiels du cours)
    - drills_solver.py       (Générateur & solveur : Fragmentation MTU, Checksum Hexa, Routage LPM)
    - tips_bank.py           (Banque de conseils style Minecraft & gestion du Streak / Advancements)
  - ui/                      (Interface graphique PyQt6)
    - __init__.py
    - themes.py              (Feuilles de style QSS : Light Mode & Hacker Dark Mode)[cite: 2]
    - widgets.py             (IpLineEdit amélioré, MinecraftTipBanner, AdvancementToast)
    - main_window.py         (Fenêtre principale, barre d'onglets, Streak badge, Theme toggle)
    - tab_binary.py          (Onglet 1 : Convertisseur 8-bit + Inspecteur de Masque)
    - tab_subnet.py          (Onglet 2 : Subnet Practice + Classification + Tiroir Binaire)
    - tab_vlsm.py            (Onglet 3 : VLSM Express avec saisie minimale + Auto-complétion)
    - tab_drills.py          (Onglet 4 : Flash Drills — Fragmentation MTU, Checksum & Routage LPM)

---

## 3. Spécifications du Moteur (`engine/`) & Formules du Cours

### 3.1. `engine/ipv4_math.py`
Doit fournir des fonctions/classes pures pour :
1. Inspection d'un octet (0 à 255) :
   - `is_valid_mask_octet(val: int) -> bool` : Vrai si `val in (255, 254, 252, 248, 240, 224, 192, 128, 0)` (contiguïté des bits à 1)[cite: 84].
   - `ones_complement_octet(val: int) -> int` : `(~val) & 0xFF` (soit `255 - val`).
   - `block_size_octet(val: int) -> int` : `256 - val` (le pas ou Magic Number).
2. Classification IPv4 & Portée (selon le cours) :
   - Classes (basées sur le 1er octet)[cite: 82] :
     - `Classe A` : `0` à `127` (Masque par défaut `/8`, bits de poids fort `0...`)[cite: 82]
     - `Classe B` : `128` à `191` (Masque par défaut `/16`, bits de poids fort `10...`)[cite: 82, 88]
     - `Classe C` : `192` à `223` (Masque par défaut `/24`, bits de poids fort `110...`)[cite: 82, 84]
     - `Classe D` : `224` à `239` (Multicast / diffusion de groupe, bits `1110...`)[cite: 82]
     - `Classe E` : `240` à `255` (Réservé pour un usage futur, bits `11110...`)[cite: 82]
   - Types / Portées d'adresses[cite: 82, 83] :
     - `Privée` : `10.0.0.0/8`, `172.16.0.0/12` (`172.16.0.0` à `172.31.255.255`), `192.168.0.0/16`[cite: 82, 83].
     - `Boucle locale (Loopback)` : `127.0.0.0/8`[cite: 82, 83].
     - `APIPA` : `169.254.0.0/16` (utilisée lorsqu'une machine ne parvient pas à obtenir une adresse via DHCP)[cite: 83].
     - `Publique` : Toutes les autres adresses unicast routables sur Internet[cite: 83].
3. Calculs de Sous-Réseau & Opérations Binaires :
   - `Network Address` : Obtenue en appliquant l'opérateur `ET` binaire entre l'adresse IPv4 et le masque de sous-réseau (`IP AND Mask`)[cite: 85].
   - `Host ID Interne` : Obtenue en appliquant l'opérateur `ET` binaire entre l'adresse IPv4 et le complément à un du masque (`IP AND (~Mask & 0xFFFFFFFF)`)[cite: 85].
   - `Broadcast Address` : Dernière adresse de la plage (la partie hôte ne contient que des bits à 1)[cite: 85].
   - `First Host` : `Network + 1` | `Last Host` : `Broadcast - 1` | `Next Subnet` : `Broadcast + 1`[cite: 2].
   - Bits empruntés (`b_S`) et Hôtes disponibles (`b_H`)[cite: 87, 88] :
     - Par rapport au masque par défaut de la classe (`A=/8`, `B=/16`, `C=/24`), si `CIDR >= default_cidr`, alors `b_S = CIDR - default_cidr`, donnant `2^b_S` sous-réseaux possibles et `2^(32 - CIDR) - 2` hôtes disponibles par sous-réseau (exemple du cours : `154.4.32.0/19` -> Classe B `/16`, `b_S = 19 - 16 = 3` -> `2^3 = 8` sous-réseaux possibles et `2^13 - 2 = 8190` hôtes possibles)[cite: 87, 88].

### 3.2. `engine/vlsm_solver.py`
Implémente l'algorithme de découpage VLSM[cite: 86, 89, 90, 91, 92, 93] :
1. Trier les besoins en machines par ordre strictement décroissant (du plus grand sous-réseau au plus petit)[cite: 90, 93].
2. Pour chaque besoin `N` machines, trouver la plus petite puissance `h` telle que `2^h - 2 >= N` (soit `N + 2 <= 2^h` adresses nécessaires en comptant réseau et diffusion)[cite: 89, 92, 95, 96].
3. Calculer le préfixe `CIDR = 32 - h`, la taille du bloc `2^h`, et allouer séquentiellement à partir de l'adresse de base[cite: 90, 92, 93].
4. Inclure 3 modes/presets dans le générateur :
   - `Preset Cours 1` : Réseau `193.225.34.0/24` avec besoins `[44, 20, 100]` -> Trié : 100 machines (`/25` ou `255.255.255.128`, `193.225.34.0` à `.127`), 44 machines (`/26` ou `255.255.255.192`, `193.225.34.128` à `.191`), 20 machines (`/27` ou `255.255.255.224`, `193.225.34.192` à `.223`)[cite: 89, 90, 91].
   - `Preset Cours 2` : Réseau `192.168.0.0/24` avec besoins `[100, 28, 4]` -> Trié : 100 machines (`/25`, `192.168.0.0/25`, plage `192.168.0.1` à `192.168.0.126`), 28 machines (`/27`, `192.168.0.128/27`, plage `192.168.0.129` à `192.168.0.158`), 4 machines (`/29`, `192.168.0.160/29`, plage `192.168.0.161` à `192.168.0.166`)[cite: 94, 95, 96].
   - `Aléatoire` : Génère un réseau `/24` privé et 3 besoins aléatoires dont la somme des blocs est `<= 256`.

### 3.3. `engine/drills_solver.py`
Contient les générateurs et validateurs pour les 3 mini-exercices rapides du cours :
1. Drill 1 — Fragmentation IPv4 & MTU[cite: 97, 98, 99, 107, 108, 109, 153, 154, 155] :
   - Paramètres : `total_length` (ex: `4000` ou `5000`), `ihl` (ex: `5`), `mtu` (ex: `1500`)[cite: 107, 155].
   - Formules :
     - `Header Length = IHL * 4` octets (ex: `5 * 4 = 20` octets)[cite: 97, 104, 108].
     - `Données Originales = Total Length - Header Length` (ex: `4000 - 20 = 3980` octets)[cite: 106, 108].
     - `Max Données par Fragment = ((MTU - Header Length) // 8) * 8` (doit être un multiple de 8 octets, ex: `1500 - 20 = 1480`, divisible par 8 car `1480 / 8 = 185`)[cite: 99, 108, 154].
     - Pour chaque fragment : calculer `payload`, `fragment_offset` (position en unités de 8 octets : `0`, `185`, `370`...), et `mf_flag` (`1` si d'autres fragments suivent, `0` pour le dernier fragment)[cite: 99, 108, 109, 154].
   - Inclure le bouton pour charger l'exercice officiel du cours (`Total Length = 4000`, `IHL = 5`, `MTU = 1500` -> 3 fragments de `1480`, `1480`, `1020` octets ; Offsets `0`, `185`, `370` ; MF `1`, `1`, `0`)[cite: 107, 108, 109].
2. Drill 2 — Routage & Longest Prefix Match (LPM)[cite: 123, 124, 125, 127, 128, 129, 130, 131, 132, 133, 134] :
   - Génère une table de routage de 4 à 5 entrées (`Code`, `Destination/CIDR`, `[AD/Métrique]`, `Next Hop`, `Interface`) et une adresse IP de destination[cite: 123, 124, 127, 133].
   - Logique de sélection du routeur[cite: 125] :
     1. Filtrer les routes qui correspondent à l'IP de destination[cite: 125, 133, 134].
     2. Règle 1 (Longest Prefix Match) : Choisir la route ayant le préfixe `/CIDR` le plus long, donc le plus spécifique (ex: `/24 > /16 > /8 > /0`)[cite: 125, 129, 130, 133, 134].
     3. Règle 2 (Distance Administrative - AD) : Si plusieurs routes ont le même préfixe `/CIDR` mais proviennent de protocoles différents, choisir la plus petite AD (`Connected = 0`, `Static = 1`, `OSPF = 110`, `RIP = 120`)[cite: 123, 125, 127, 131, 132].
     4. Règle 3 (Métrique) : Si même préfixe et même protocole, choisir la plus petite métrique[cite: 123, 125, 132].
3. Drill 3 — Somme de Contrôle de l'En-tête IPv4 (Header Checksum 16 bits)[cite: 100, 113, 114, 115, 116, 117, 118] :
   - Diviser l'en-tête en mots de 16 bits (avec le champ Checksum mis à 0) et les additionner[cite: 100, 113, 114, 115].
   - Gérer le dépassement (end-around carry) : si la somme dépasse `0xFFFF`, additionner la retenue de poids fort aux 16 bits de poids faible[cite: 113, 116].
   - Prendre le complément à un du résultat final : `checksum = (~s) & 0xFFFF`[cite: 100, 113, 117].
   - Inclure l'exemple exact du cours : `4500 0054 0000 4000 4001 0000 C0A8 0068 C0A8 0001` -> Somme `0x2470E` -> Dépassement `0x470E + 0x2 = 0x4710` -> Complément à un `0xB8EF`[cite: 114, 115, 116, 117, 118].

---

## 4. Spécifications de l'Interface (`ui/`) & Style Minecraft

### 4.1. Composants Globaux (`ui/widgets.py`)
1. `IpLineEdit` (Smart Auto-Dot v1.2.0) :
   - Conserver le comportement existant : `Espace` ou `Virgule` insère un `.` ou saute par-dessus un `.` existant ; 3 chiffres insèrent automatiquement un `.`[cite: 2].
   - Amélioration v1.2.0 : Si l'utilisateur tape 2 chiffres dans l'octet courant et que `int(octet) >= 26` (ex: `32`, `99`), insérer immédiatement le `.` sans attendre un 3ème chiffre.
2. `MinecraftTipBanner` (Bannière d'astuces en bas de fenêtre) :
   - Barre stylisée façon Splash Text / Tooltip de Minecraft en bas de `MainWindow`.
   - Affiche une astuce avec son préfixe (`[⚡ APP TIP]`, `[🧠 COURS INPT]`, `[🔥 ASTUCE PRO]`).
   - Change automatiquement toutes les 12 secondes via `QTimer` ou au clic sur le bouton `"🎲 Astuce"` / sur la bannière.
   - Inclure au moins 15 astuces couvrant les raccourcis clavier de l'app et les notions clés du cours (octets contigus du masque `255, 254, 252, 248, 240, 224, 192, 128, 0`, règle d'or VLSM du plus grand au plus petit, Offset en unités de 8 octets, AD OSPF 110 vs RIP 120, APIPA `169.254.0.0/16`, Loopback `127.0.0.0/8`)[cite: 82, 83, 84, 90, 99, 131, 132].
3. Système de Streak & Notification `"🏆 Progrès débloqué !"` :
   - Afficher un compteur `🔥 Série : X` à côté du bouton de thème dans la barre d'onglets.
   - Quand un exercice est entièrement validé sans avoir cliqué sur `"Show"`, incrémenter la série et afficher un bandeau style Minecraft Advancement pendant 3 secondes (ex: `🏆 Progrès débloqué : [Architecte VLSM]`).

### 4.2. Organisation des 4 Onglets (Clairs et Aérés)
1. Onglet 1 — `BinaryConverterTab` (`Convertisseur 8-Bit`) :
   - Garde l'interface actuelle (8 cartes de bits cliquables `128..1` + synchronisation Binaire / Décimal / Hexa + boutons presets)[cite: 2].
   - Ajoute en dessous une barre compacte "Inspecteur de Masque & Complément" (en lecture seule, zéro saisie) qui affiche en direct :
     - `Octet de masque valide ?` (`Oui` en vert si contigu, sinon `Non`)[cite: 84]
     - `Complément à 1 (~X)` en décimal et binaire[cite: 85]
     - `Pas du sous-réseau (256 - X)`
2. Onglet 2 — `SubnetPracticeTab` (`Pratique Sous-Réseau`) :
   - Garde le tableau principal à 5 lignes (`Network`, `First Host`, `Last Host`, `Broadcast`, `Next Subnet`)[cite: 2].
   - Ajoute sous la barre de l'IP cible 2 petits sélecteurs rapides (`Classe : [A | B | C]` et `Type : [Publique | Privée | APIPA | Loopback]`) avec validation instantanée `✓ / ✕`[cite: 82, 83].
   - Ajoute un bouton `🔍 Afficher le détail binaire (32 bits)` (replié par défaut) qui montre l'opération `IP ET Masque`, le `Host ID (IP ET ~Masque)`, le nombre de bits empruntés `b_S` et le nombre d'hôtes disponibles `2^b_H - 2`[cite: 85, 87, 88].
3. Onglet 3 — `VlsmLabTab` (`Atelier VLSM Express`) :
   - Affiche le réseau de base `/24` et 3 besoins en machines (dans le désordre) avec boutons : `"Nouveau VLSM"`, `"📘 Ex. Cours 1 (100, 44, 20)"`, `"📘 Ex. Cours 2 (100, 28, 4)"`[cite: 89, 94].
   - Tableau de 3 lignes (du plus grand au plus petit besoin)[cite: 90, 93] :
     - L'utilisateur saisit uniquement : `Besoin choisi (Machines)`, `/CIDR` et `Adresse Réseau (Network IP)`[cite: 90, 92, 93].
     - Dès que `/CIDR` et `Network IP` sont corrects sur une ligne (`✓`), l'application remplit automatiquement la colonne de résumé : `Plage : .1 -> .126 | Broadcast : .127 | Masque : .128`[cite: 90, 95, 96].
4. Onglet 4 — `FlashDrillsTab` (`Quiz Express : MTU, Routage & Checksum`) :
   - Barre de sélection de mini-exercice en haut de l'onglet : `[ 📦 Fragmentation MTU | 🧭 Routage LPM | 🧮 Checksum Hexa ]`.
   - N'affiche qu'un seul mini-exercice à la fois pour garder l'écran très aéré :
     - Vue Fragmentation MTU : Énoncé (`Total Length`, `IHL`, `MTU`) + bouton `"📘 Ex. Cours (4000B)"` + tableau de 3 lignes où l'utilisateur saisit `Données (octets)`, `Offset (/8)` et `MF (0/1)`[cite: 107, 108, 109].
     - Vue Routage LPM : Table de routage de 4 routes + IP de destination + sélection de la route gagnante et de la règle appliquée (`Longest Prefix Match`, `Distance Administrative (AD)`, `Métrique`, `Route par défaut`)[cite: 125, 129, 130, 131, 132, 133, 134].
     - Vue Checksum Hexa : Mots de 16 bits (mode court 4 mots ou bouton `"📘 Ex. Cours 10 mots"`) + saisie de la somme brute, de la somme avec retenue (end-around carry) et du complément à un final[cite: 113, 114, 115, 116, 117].

---

## 5. Plan d'Exécution Séquentiel pour l'Agent
Exécute ce cahier des charges dans l'ordre exact suivant :
1. Phase 1 : Créer le dossier `engine/` (`__init__.py`, `ipv4_math.py`, `vlsm_solver.py`, `drills_solver.py`, `tips_bank.py`) et vérifier par un test rapide en console que tous les cas du cours donnent les résultats exacts.
2. Phase 2 : Créer `ui/themes.py` et `ui/widgets.py` (`IpLineEdit` avec auto-dot `>= 26`, `MinecraftTipBanner`, `AdvancementToast`) ainsi que les onglets 1 (`ui/tab_binary.py`) et 2 (`ui/tab_subnet.py`).
3. Phase 3 : Créer les onglets 3 (`ui/tab_vlsm.py`) et 4 (`ui/tab_drills.py`), puis assembler le tout dans `ui/main_window.py` et mettre à jour `converter.py`[cite: 2].
4. Phase 4 : Lancer et tester `python converter.py` pour vérifier l'absence d'erreurs d'import ou de signaux PyQt6, puis mettre à jour `README.md`[cite: 1, 2].