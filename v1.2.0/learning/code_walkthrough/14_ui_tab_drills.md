# 📄 Guide de Fichier : `ui/tab_drills.py`

Le fichier [`ui/tab_drills.py`](file:///c:/Users/lenovo/Desktop/laformatik/ipv4-subnet-toolkit/v1.2.0/ui/tab_drills.py) implémente l'**Onglet 4 : Flash Drills — Mini-Exercices Express du Cours INPT** :
1. **📦 Fragmentation MTU** (IHL, multiple de 8 octets, calcul du champ Offset, drapeau MF).
2. **🧭 Routage LPM & Distance Administrative** (Table de 4 routes, choix de la route gagnante et de la règle décisive).
3. **🧮 Checksum d'En-tête IPv4 (16 bits)** (Somme brute, report de retenue *End-Around Carry*, complément à un final).

---

## 1. Rôle dans l'Architecture (Patron QStackedWidget & Zero Clutter)

Rassembler 3 exercices techniques distincts sur un même écran sans surcharger l'utilisateur nécessite une architecture de navigation propre.

`FlashDrillsTab` utilise un composant **`QStackedWidget`** (pile d'écrans) :
- Une barre de navigation supérieure (`drillNavBtn`) permet de choisir le mini-exercice.
- **Un seul exercice est affiché à la fois** (`self.stack.setCurrentIndex(i)`).
- Aucun défilement vertical parasite n'est nécessaire.

```
FlashDrillsTab (QVBoxLayout)
 ├── nav_card (QHBoxLayout) : [📦 Fragmentation MTU] [🧭 Routage LPM] [🧮 Checksum Hexa]
 └── stack: QStackedWidget
      ├── Page 0: _build_mtu_page()      (Fragmentation IPv4)
      ├── Page 1: _build_lpm_page()      (Table de routage & LPM)
      └── Page 2: _build_checksum_page() (Calcul de Checksum 16-bit)
```

---

## 2. Bibliothèques et Modules Importés

```python
from typing import Callable, Dict, List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QStackedWidget, QLabel, QLineEdit, QPushButton, QFrame
)
from PyQt6.QtCore import Qt

from engine.drills_solver import (
    ChecksumProblem, DrillsSolver, LpmProblem, MtuProblem
)
```

- **`engine.drills_solver.DrillsSolver`** : Fournit les algorithmes et les presets officiels de fragmentation, de routage et de somme hexadécimale.
- **`QStackedWidget`** : Conteneur dynamique affichant une seule vue à la fois parmi les 3 pages empilées.

---

## 3. Analyse de la Page 1 : Fragmentation MTU (`_build_mtu_page`)

### 3.1. Composants Graphiques
- **Bandeau Supérieur** : Affiche les paramètres du paquet d'origine :
  - Longueur totale (ex: `4000 octets`).
  - Champ IHL (ex: `5`, soit $5 \times 4 = 20 \text{ octets}$ d'en-tête).
  - MTU du lien de sortie (ex: `1500 octets`).
  - Boutons : `📘 Ex. Cours 4000B` et `🎲 Aléatoire`.
- **Grille de Saisie des Fragments** : 3 lignes de fragments comprenant chacune :
  - Charge utile (ex: `1480`).
  - Déplacement (*Fragment Offset*, division par 8, ex: `0`, `185`, `370`).
  - Drapeau MF (*More Fragments*, `1` ou `0`).
  - Indicateur de statut `✓` ou `✕`.
  - Bouton `Show` d'aide.

### 3.2. Validation d'un Fragment : `validate_mtu_row(row_idx)`
```python
def validate_mtu_row(self, row_idx: int):
    frag = self.current_mtu.fragments[row_idx]
    p_txt = self.mtu_payload_inputs[row_idx].text().strip()
    o_txt = self.mtu_offset_inputs[row_idx].text().strip()
    m_txt = self.mtu_mf_inputs[row_idx].text().strip()

    is_ok = (
        p_txt.isdigit() and int(p_txt) == frag.payload_bytes
        and o_txt.isdigit() and int(o_txt) == frag.offset_units
        and m_txt.isdigit() and int(m_txt) == frag.mf_flag
    )
    self._set_status(self.mtu_status_labels[row_idx], is_ok)
```
- L'étudiant doit avoir trouvé à la fois la bonne charge utile (multiple de 8), le bon offset (position divisée par 8) et le bon drapeau MF pour que la ligne soit validée.
- Succès débloqué : **"Chirurgien MTU"** (`"mtu_clean"`).

---

## 4. Analyse de la Page 2 : Routage IP & Longest Prefix Match (`_build_lpm_page`)

### 4.1. Composants Graphiques
- **Bandeau de Destination** : Affiche l'adresse IP du paquet entrant à router (ex: `192.168.12.45`).
- **Table de Routage à 4 Routes** :
  - Colonne 1 : Code protocole (`C` pour connecté, `S` pour statique, `O` pour OSPF, `R` pour RIP, `S*` pour route par défaut).
  - Colonne 2 : Préfixe réseau (ex: `192.168.12.0/24`).
  - Colonne 3 : Distance Administrative et Métrique (ex: `[110/20]`).
  - Colonne 4 : Prochain saut (*Next-Hop*) ou interface de sortie.
- **Questions Interactives (Choix Multiples)** :
  1. *Quelle route l'emporte ?* Boutons `Route #1`, `Route #2`, `Route #3`, `Route #4`.
  2. *Pourquoi (règle décisive) ?* Boutons `Longest Prefix Match`, `Distance Administrative (AD)`, `Métrique`, `Route par défaut`.
- **Cartouche d'Explication Pédagogique** (`lbl_lpm_feedback`) : Dès que les deux choix sont sélectionnés, l'application explique en détail le raisonnement du routeur (ex: pourquoi le préfixe prime sur la distance administrative).

### 4.2. Validation du Routage : `validate_lpm_selection()`
```python
def validate_lpm_selection(self):
    if self.selected_route_id is None or self.selected_rule is None:
        return
    route_ok = (self.selected_route_id == self.current_lpm.winning_row_id)
    rule_ok = (self.selected_rule == self.current_lpm.decisive_rule)

    if route_ok and rule_ok:
        self.lbl_lpm_feedback.setText(f"✓ EXCELLENT ! {self.current_lpm.explanation}")
        if not self.lpm_rewarded and not self.lpm_used_show:
            self.lpm_rewarded = True
            if self.on_clean_solve:
                self.on_clean_solve("lpm_clean")
    else:
        self.lbl_lpm_feedback.setText(f"✕ INCORRECT. {self.current_lpm.explanation}")
```
- Succès débloqué : **"Routeur Humain"** (`"lpm_clean"`).

---

## 5. Analyse de la Page 3 : Checksum IPv4 16 bits (`_build_checksum_page`)

### 5.1. Composants Graphiques
- **Mots Hexadécimaux de l'En-Tête** :
  - Mode Cours : Les 10 mots de 16 bits officiels de l'INPT (`4500 0054 0000 4000 4001 0000 C0A8 0068 C0A8 0001`).
  - Mode Court : 4 mots hexadécimaux aléatoires générant au moins une retenue au-delà de 16 bits.
- **Carte de Résolution en 3 Étapes Guidées** :
  1. **Étape 1** : Somme hexadécimale brute (ex: `0x2470E`).
  2. **Étape 2** : Après rabattement de retenue *End-Around Carry* (ex: `0x4710`).
  3. **Étape 3** : Complément à un final / Checksum (ex: `0xB8EF`).

### 5.2. Validation du Checksum : `validate_checksum()`
```python
def validate_checksum(self):
    raw_val = DrillsSolver.parse_hex_input(self.chk_inputs["raw"].text())
    car_val = DrillsSolver.parse_hex_input(self.chk_inputs["carried"].text())
    fin_val = DrillsSolver.parse_hex_input(self.chk_inputs["final"].text())

    raw_ok = (raw_val == self.current_chk.raw_sum)
    car_ok = (car_val == self.current_chk.carried_sum)
    fin_ok = (fin_val == self.current_chk.checksum)

    self._set_status(self.chk_status["raw"], raw_ok)
    self._set_status(self.chk_status["carried"], car_ok)
    self._set_status(self.chk_status["final"], fin_ok)
```
- Chaque étape est corrigée indépendamment, permettant à l'étudiant de localiser précisément si son erreur provient de l'addition de base, du décalage de la retenue ou de l'inversion binaire.
- Succès débloqué : **"Seigneur du Checksum"** (`"checksum_clean"`).
