# 📄 Guide de Fichier : `ui/tab_binary.py`

Le fichier [`ui/tab_binary.py`](file:///c:/Users/lenovo/Desktop/laformatik/ipv4-subnet-toolkit/v1.2.0/ui/tab_binary.py) implémente l'**Onglet 1 : Convertisseur Binaire 8-Bit & Inspecteur de Masque**.

Ce module permet aux étudiants d'acquérir les réflexes de calcul binaire indispensables au découpage d'adresses IPv4 : addition des puissances de 2, conversion binaire/décimal/hexadécimal bidirectionnelle en direct, contiguïté des bits d'un octet de masque, et calcul du complément à un (~X).

---

## 1. Rôle dans l'Architecture & Pédagogie

Dans le cours de réseaux de l'INPT, toute la difficulté du sous-réseau provient d'une mauvaise maîtrise des 8 bits d'un octet.
L'onglet 1 élimine cette barrière en proposant une triple synchronisation en temps réel :
1. **Manipuler visuellement les 8 bits** via des cases à cocher associées aux poids $2^7$ (128) jusqu'à $2^0$ (1).
2. **Saisir librement dans n'importe quel format** : Binaire (`"11000000"`), Décimal (`"192"`), ou Hexadécimal (`"0xC0"`), les deux autres s'ajustant instantanément.
3. **Inspecter en direct la validité du masque** : Indique immédiatement si l'octet saisi est un octet de masque valide (bits à 1 contigus), son complément à 1 (Wildcard) et son pas de sous-réseau (Magic Number $256 - X$).

---

## 2. Bibliothèques et Modules Importés

```python
from typing import List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QCheckBox, QPushButton, QFrame
)
from PyQt6.QtCore import Qt

from engine.ipv4_math import IPv4MathEngine
```

- **`engine.ipv4_math.IPv4MathEngine`** : C'est le moteur pur qui calcule les conversions, vérifie si l'octet appartient aux masques valides (`is_valid_mask_octet`) et calcule le pas ($256 - X$). L'interface se contente de restituer graphiquement les données du moteur.

---

## 3. Structure Visuelle & Composants de l'Onglet

L'interface se découpe en 4 cartes verticales :
1. **Header Card** : Titre et sous-titre explicatif.
2. **Main Card (Conteneur Central)** :
   - **Rangée des 8 Cartes de Bits** : 8 boîtes carrées (`#bitBox`) affichant le poids (128, 64, 32, 16, 8, 4, 2, 1), la case à cocher, et l'indice de position (Bit 7 à Bit 0).
   - **Trio de Champs de Saisie Synchronisés** :
     - Champ Binaire (`self.bin_input`)
     - Champ Décimal (`self.dec_input`)
     - Champ Hexadécimal (`self.hex_input`)
   - **Barre d'Outils & Presets Rapides** : Boutons *All 1s (255)*, *Clear All (0)*, *Inverser (~X)*, et boutons de masques usuels (*128*, *192*, *224*, *240*, *248*, *252*).
3. **Inspector Card (Inspecteur de Masque & Complément)** :
   - Colonne 1 : Octet de masque valide ? (`✓ Oui (bits contigus)` ou `✕ Non (1 et 0 alternés)`).
   - Colonne 2 : Complément à un ($\sim X = 255 - X$) avec son écriture binaire.
   - Colonne 3 : Pas du sous-réseau ($256 - X$ / Magic Number).

---

## 4. Analyse Technique du Code

### 4.1. Le Drapeau Anti-Boucle Infinie : `self._updating`
```python
class BinaryConverterTab(QWidget):
    def __init__(self):
        super().__init__()
        self.bit_values: List[int] = [128, 64, 32, 16, 8, 4, 2, 1]
        self._updating = False
```
- **Pourquoi `self._updating` est-il vital ?**
  - Lorsque l'utilisateur tape `"192"` dans `dec_input`, le signal `textEdited` déclenche la méthode `apply_value(192)`.
  - Cette méthode met à jour `bin_input.setText("11000000")` et coche les cases 128 et 64.
  - Sans le verrou `self._updating = True`, la modification de `bin_input` déclencherait à son tour son signal de modification, qui rappellerait `apply_value`, créant une **boucle récursive infinie** (stack overflow) qui ferait planter l'application.

### 4.2. Méthode Centrale : `apply_value(val: int, source: str = "")`
```python
def apply_value(self, val: int, source: str = ""):
    analysis = IPv4MathEngine.analyze_octet(val)
    self.current_value = analysis.value

    self._updating = True
    try:
        # 1. Mise à jour des 8 cases à cocher et du style de leurs cartes
        for i, bit_val in enumerate(self.bit_values):
            is_on = bool(analysis.value & bit_val)
            if self.checkboxes[i].isChecked() != is_on:
                self.checkboxes[i].setChecked(is_on)
            self.bit_cards[i].setProperty("active", is_on)
            self.bit_cards[i].style().unpolish(self.bit_cards[i])
            self.bit_cards[i].style().polish(self.bit_cards[i])

        # 2. Mise à jour des champs textes (sauf la source qui a déclenché l'événement)
        if source != "binary":
            self.bin_input.setText(analysis.binary_str)
        if source != "decimal":
            self.dec_input.setText(str(analysis.value))
        if source != "hex":
            self.hex_input.setText(analysis.hex_str)

        # 3. Mise à jour dynamique de l'inspecteur de masque
        if analysis.is_valid_mask_octet:
            self.lbl_valid_mask.setText("✓ Oui (bits à 1 contigus)")
            self.lbl_valid_mask.setObjectName("inspectorValueValid")
        else:
            self.lbl_valid_mask.setText("✕ Non (1 et 0 alternés)")
            self.lbl_valid_mask.setObjectName("inspectorValueInvalid")
        self.lbl_valid_mask.style().unpolish(self.lbl_valid_mask)
        self.lbl_valid_mask.style().polish(self.lbl_valid_mask)

        self.lbl_complement.setText(
            f"{analysis.ones_complement}  ({analysis.ones_complement_binary})"
        )
        self.lbl_block_step.setText(
            f"{analysis.block_size}  (Magic Number)"
            if analysis.is_valid_mask_octet and analysis.value > 0
            else str(analysis.block_size)
        )
    finally:
        self._updating = False
```

### 4.3. L'Astuce Qt : `style().unpolish()` et `style().polish()`
- Lorsqu'une propriété QSS dynamique change (ex: `self.bit_cards[i].setProperty("active", is_on)`), Qt ne recalcule pas automatiquement le style du widget pour des raisons de performance.
- Les appels conjoints `unpolish(widget)` puis `polish(widget)` forcent le moteur de rendu Qt à réévaluer les sélecteurs QSS (`#bitBox[active="true"]`), illuminant la carte de bit en bleu royal ou en vert néon instantanément.

### 4.4. Gestionnaires de Saisie Réactifs
- **`on_checkbox_toggled()`** : Somme les puissances de 2 actives :
  ```python
  total = sum(self.bit_values[i] for i, cb in enumerate(self.checkboxes) if cb.isChecked())
  self.apply_value(total, source="checkbox")
  ```
- **`on_binary_edited(text)`** : Filtre les caractères pour ne garder que les 8 premiers `0` ou `1`, puis convertit en base 2 via `int(filtered, 2)`.
- **`on_decimal_edited(text)`** : Clampe l'entier entre 0 et 255.
- **`on_hex_edited(text)`** : Supprime le préfixe optionnel `"0x"` et convertit en base 16 via `int(cleaned, 16)`.
- **`invert_bits()`** : Applique le complément à un via `IPv4MathEngine.ones_complement_octet(self.current_value)`.
