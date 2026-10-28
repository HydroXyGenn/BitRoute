# 📄 Guide de Fichier : `ui/main_window.py`

Le fichier [`ui/main_window.py`](file:///c:/Users/lenovo/Desktop/laformatik/ipv4-subnet-toolkit/v1.2.0/ui/main_window.py) constitue le **chef d'orchestre visuel** de l'application. Il instancie et agence l'ensemble des écrans, gère la barre supérieure de séries et trophées, le basculement de thème et la bannière d'astuces inférieure.

---

## 1. Rôle dans l'Architecture (Composite Root & Mediator)

`MainWindow` hérite de `QMainWindow` et joue deux rôles architecturaux fondamentaux :
1. **Racine de Composition (Composite Root)** : C'est le seul endroit où tous les onglets (`tab_binary`, `tab_subnet`, `tab_vlsm`, `tab_drills`), le conteneur d'onglets (`QTabWidget`), le gestionnaire d'astuces (`TipsAndStreakManager`), et les bannières sont créés et assemblés dans un layout vertical unifié.
2. **Médiateur d'Événements (Mediator Pattern)** : Lorsqu'un sous-onglet résout proprement un exercice (sans cliquer sur *"Show"*), il n'accède pas directement aux labels de la fenêtre principale. Il invoque une fonction de rappel (*callback*) `on_clean_solve` transmise par `MainWindow`. `MainWindow` intercepte l'événement, met à jour le compteur de flammes `🔥 Série : N` et déclenche le toast doré.

---

## 2. Bibliothèques et Modules Importés

```python
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton
)
from PyQt6.QtCore import Qt

from engine.tips_bank import TipsAndStreakManager
from ui.themes import get_dark_qss, get_light_qss
from ui.widgets import AdvancementToast, MinecraftTipBanner
from ui.tab_binary import BinaryConverterTab
from ui.tab_subnet import SubnetPracticeTab
from ui.tab_vlsm import VlsmLabTab
from ui.tab_drills import FlashDrillsTab
```

- **`QMainWindow`** : Fenêtre principale standard de Qt offrant la gestion d'un widget central (`setCentralWidget`), de menus et de barres d'outils.
- **`QTabWidget`** : Conteneur à onglets empilés permettant de basculer instantanément entre les 4 modules du cours sans recharger de fenêtre.
- **`ui.themes`** : Fournit `get_light_qss()` et `get_dark_qss()`.

---

## 3. Structure Visuelle & Agencement (Layout Hierarchy)

L'arbre des composants de `MainWindow` est organisé comme suit :

```
QMainWindow
 └── root_widget (QVBoxLayout, margins=0, spacing=0)
      ├── toast_wrapper (QHBoxLayout, margins=16, 6, 16, 0)
      │    └── AdvancementToast (bannière dorée masquée par défaut)
      │
      ├── tabs: QTabWidget (stretch=1, occupe tout l'espace central)
      │    ├── CornerWidget (TopRightCorner) :
      │    │    ├── lbl_streak ("🔥 Série : 0")
      │    │    └── btn_dark_toggle ("💻 Hacker Dark", fixedWidth=135)
      │    │
      │    ├── Tab 0: BinaryConverterTab ("1. Convertisseur 8-Bit")
      │    ├── Tab 1: SubnetPracticeTab  ("2. Pratique Sous-Réseau")
      │    ├── Tab 2: VlsmLabTab         ("3. Atelier VLSM Express")
      │    └── Tab 3: FlashDrillsTab     ("4. Flash Drills (MTU, LPM, Hex)")
      │
      └── tip_banner: MinecraftTipBanner (bannière verte/sombre en bas)
```

---

## 4. Analyse Méthode par Méthode

### 4.1. `__init__()`
1. **Configuration de la Fenêtre** :
   ```python
   self.setWindowTitle("IPv4 Subnet Toolkit v1.2.0 — INPT ASEDS Edition")
   self.resize(1100, 720)
   self.setMinimumSize(980, 620)
   self.is_dark_mode = False
   ```
   Définit un titre clair, une dimension par défaut confortable de $1100 \times 720$ pixels, et une taille minimale de $980 \times 620$ pour empêcher les chevauchements de contrôles lors du redimensionnement par l'utilisateur.
2. **Injection de Dépendances vers les Onglets** :
   ```python
   self.tab_subnet = SubnetPracticeTab(on_clean_solve=self.handle_clean_solve)
   self.tab_vlsm = VlsmLabTab(on_clean_solve=self.handle_clean_solve)
   self.tab_drills = FlashDrillsTab(on_clean_solve=self.handle_clean_solve)
   ```
   Chaque onglet d'exercices reçoit en paramètre la méthode `handle_clean_solve`.
3. **Le Widget de Coin (`TopRightCorner`)** :
   ```python
   self.tabs.setCornerWidget(corner_widget, Qt.Corner.TopRightCorner)
   ```
   Qt permet de loger des boutons directement à droite de la barre d'onglets. C'est ici que sont placés le badge de série `🔥` et le bouton de basculement de thème.
4. **Verrouillage de Largeur du Bouton de Thème** :
   ```python
   self.btn_dark_toggle.setFixedWidth(135)
   ```
   *Raisonnement Ergonomique* : Lorsque l'intitulé du bouton bascule de `"💻 Hacker Dark"` à `"☀️ Light Mode"`, la chaîne a une largeur de texte différente. Sans `setFixedWidth(135)`, le bouton rétrécirait ou s'élargirait, décalant légèrement les onglets à sa gauche. La largeur fixe garantit une immobilité totale (0 pixel de shift).

### 4.2. `handle_clean_solve(category_key: str)`
```python
def handle_clean_solve(self, category_key: str):
    adv = self.tips_manager.record_clean_solve(category_key)
    self.lbl_streak.setText(f"🔥 Série : {self.tips_manager.streak}")
    if adv is not None:
        self.advancement_toast.show_advancement(adv, self.tips_manager.streak)
```
- Appelée automatiquement par les onglets lorsqu'un problème est résolu sans aide.
- Met à jour l'étiquette de série dans le coin supérieur droit.
- Déclenche l'animation du toast si un nouveau trophée est débloqué.

### 4.3. `toggle_dark_mode()` & `apply_theme()`
```python
def toggle_dark_mode(self):
    self.is_dark_mode = not self.is_dark_mode
    if self.is_dark_mode:
        self.btn_dark_toggle.setText("☀️ Light Mode")
    else:
        self.btn_dark_toggle.setText("💻 Hacker Dark")
    self.apply_theme()

def apply_theme(self):
    if self.is_dark_mode:
        self.setStyleSheet(get_dark_qss())
    else:
        self.setStyleSheet(get_light_qss())
```
- Inverse l'indicateur booléen `is_dark_mode`.
- Met à jour le texte du bouton.
- Applique la feuille de style QSS globale via `self.setStyleSheet(...)`, qui se propage instantanément par cascade à l'ensemble des enfants de la fenêtre.
