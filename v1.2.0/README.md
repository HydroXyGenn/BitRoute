# 🌐 IPv4 Subnet Toolkit v1.2.0 — INPT ASEDS Edition

Une application de bureau modulaire construite avec **Python** et **PyQt6** pour maîtriser l'adressage IPv4, le découpage en sous-réseaux, le **VLSM**, la **fragmentation MTU**, le **routage Longest Prefix Match (LPM)** et le **Checksum IPv4 16 bits**.

---

## ✨ Nouveautés majeures de la v1.2.0

### 1. 🧱 Architecture Modulaire Découplée (`engine/` vs `ui/`)
- **`engine/` (100% Python standard, ZÉRO dépendance PyQt6)** : Conçu en Programmation Orientée Objet propre (`@dataclass(frozen=True)` et méthodes statiques/pures) pour servir de modèle de référence direct en vue d'un portage Java Orienté Objet (Cursus Ingénieur ASEDS — INPT).
- **`ui/` (PyQt6)** : Interface réactive à zéro surcharge cognitive selon le principe *« Tester la décision, automatiser la répétition »*.

### 2. 🧮 Onglet 1 — Convertisseur 8-Bit & Inspecteur de Masque
- **8 cartes de bits interactives** (`128, 64, 32, 16, 8, 4, 2, 1`) + synchronisation temps réel **Binaire / Décimal / Hexadécimal**.
- **Inspecteur de Masque & Complément en direct** :
  - Vérifie si l'octet est un **octet de masque valide** (bits à `1` contigus : `255, 254, 252, 248, 240, 224, 192, 128, 0`).
  - Calcule le **Complément à 1 (`~X = 255 - X`)** en décimal et binaire.
  - Calcule le **Pas du sous-réseau (`256 - X`, Magic Number)**.

### 3. 🎯 Onglet 2 — Pratique Sous-Réseau & Tiroir Binaire 32-Bit
- **Sélecteurs rapides de Classification** : `Classe : [A | B | C]` et `Type : [Publique | Privée | APIPA | Loopback]` avec validation instantanée `✓ / ✕`.
- **Tableau à 5 lignes** : `Network`, `First Host`, `Last Host`, `Broadcast`, `Next Subnet`.
- **Divulgation Progressive (`🔍 Afficher le détail binaire 32 bits`)** : Panneau repliable affichant `IP ET Masque`, `Host ID Interne (IP ET ~Masque)`, le nombre de bits empruntés $b_S$ ($2^{b_S}$ sous-réseaux) et de bits d'hôtes $b_H$ ($2^{b_H} - 2$ machines), avec le bouton **`📘 Ex. Cours (154.4.32.0/19)`**.

### 4. 📐 Onglet 3 — Atelier VLSM Express (Zéro Surcharge)
- **Presets officiels du cours INPT** :
  - `📘 Ex. Cours 1` : `193.225.34.0/24` avec besoins `[44, 20, 100]`.
  - `📘 Ex. Cours 2` : `192.168.0.0/24` avec besoins `[28, 4, 100]`.
  - `🎲 Nouveau VLSM` : Générateur aléatoire de besoins non triés.
- **Auto-Complétion Intelligente** : L'utilisateur saisit uniquement le **Besoin trié**, le **`/CIDR`** et l'**`Adresse Réseau`**. Dès que la ligne est juste (`✓`), la plage d'hôtes utilisables, le Broadcast et le masque décimal s'affichent automatiquement.

### 5. ⚡ Onglet 4 — Flash Drills (MTU, Routage LPM & Checksum Hexa)
- **📦 Fragmentation MTU** : Calcul de la charge utile multiple de 8 octets (`((MTU - IHL*4) // 8) * 8`), de l'Offset (`/8`) et du drapeau `MF (0/1)`, incluant l'exercice du cours (`4000 octets, IHL=5, MTU=1500`).
- **🧭 Routage & Longest Prefix Match (LPM)** : Table de routage à 4 entrées testant dans l'ordre : *Longest Prefix Match*, *Distance Administrative (AD)* (`C=0, S=1, OSPF=110, RIP=120`), *Métrique* et *Route par défaut (`0.0.0.0/0`)*.
- **🧮 Checksum En-tête IPv4 (16 bits)** : Somme hexadécimale brute, rabattement de la retenue (*end-around carry*) et complément à un final (`~Somme & 0xFFFF`), incluant l'exemple officiel du cours (`0x2470E` $\rightarrow$ `0x4710` $\rightarrow$ `0xB8EF`).

### 6. 🎮 Gamification Style Minecraft & Saisie Rapide `IpLineEdit`
- **Smart Auto-Dot v1.2.0** : Insère automatiquement un `.` après 3 chiffres, à la barre d'espace/virgule, ou **dès 2 chiffres si l'octet est $\ge 26$** (ex: `32.`, `68.`, `99.`).
- **Bannière d'astuces (`MinecraftTipBanner`)** : Rotation automatique toutes les 12 secondes entre 16 astuces du cours INPT et raccourcis clavier.
- **Système de Série (`🔥 Série : X`) & Toasts (`🏆 Progrès débloqué`)** : Récompense chaque exercice résolu sans cliquer sur `Show`.

---

## 📂 Structure du Projet

```text
v1.2.0/
├── converter.py                 # Point d'entrée principal PyQt6
├── run_app.bat                  # Lanceur Windows sans console
├── run_app.vbs                  # Lanceur VBS silencieux
├── implementation.md            # Spécification technique maître v1.2.0
├── README.md                    # Documentation du projet
├── engine/                      # Moteur réseau pur (100% Python standard, zéro PyQt6)
│   ├── __init__.py
│   ├── ipv4_math.py             # Octet, classes A-E, RFC1918/APIPA/Loopback, binaire 32 bits
│   ├── vlsm_solver.py           # Algorithme de découpage VLSM & presets du cours
│   ├── drills_solver.py         # Solveurs MTU, Routage LPM/AD/Métrique, Checksum 16 bits
│   └── tips_bank.py             # Banque d'astuces & gestionnaire de Série / Progrès
├── ui/                          # Interface graphique PyQt6
│   ├── __init__.py
│   ├── themes.py                # Thèmes QSS : Light Mode & 💻 Hacker Dark (#000000 / #00FF66)
│   ├── widgets.py               # IpLineEdit (auto-dot >= 26), MinecraftTipBanner, AdvancementToast
│   ├── main_window.py           # Fenêtre principale, onglets, badge Série, switch de thème
│   ├── tab_binary.py            # Onglet 1 : Convertisseur 8-bit + Inspecteur de Masque
│   ├── tab_subnet.py            # Onglet 2 : Pratique Sous-Réseau + Tiroir Binaire 32 bits
│   ├── tab_vlsm.py              # Onglet 3 : Atelier VLSM Express avec auto-complétion
│   └── tab_drills.py            # Onglet 4 : Flash Drills (MTU, LPM, Checksum)
└── learning/                    # Notes techniques et pédagogiques détaillées
```

---

## 🚀 Exécution

```bash
pip install PyQt6
python converter.py
```
