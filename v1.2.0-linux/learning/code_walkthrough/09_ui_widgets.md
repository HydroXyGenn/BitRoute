# 📄 Guide de Fichier : `ui/widgets.py`

Le fichier [`ui/widgets.py`](file:///c:/Users/lenovo/Desktop/laformatik/ipv4-subnet-toolkit/v1.2.0/ui/widgets.py) implémente trois composants graphiques réutilisables sur-mesure héritant des classes de base de PyQt6 :
1. **`IpLineEdit`** : Champ de saisie d'adresse IPv4 avec assistance de frappe intelligente **Smart Auto-Dot**.
2. **`MinecraftTipBanner`** : Bannière inférieure rotative d'astuces et de rappels de cours (temporisation de 12 secondes).
3. **`AdvancementToast`** : Notification visuelle éphémère de succès façon Minecraft (temporisation de 3,2 secondes).

---

## 1. Bibliothèques et Modules Importés

```python
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt, QTimer
from engine.tips_bank import Advancement, TipsAndStreakManager
```

### `PyQt6.QtCore.QTimer`
- **Pourquoi `QTimer` ?** Dans une application événementielle graphique, exécuter un `time.sleep()` bloquerait complètement la boucle d'événements de l'interface (la fenêtre deviendrait blanche avec la mention *"Ne répond pas"* sous Windows).
- `QTimer` s'intègre nativement dans la boucle d'événements Qt sans bloquer le thread principal :
  - **Minuteur récurrent (`setInterval(12000)`)** : Déclenche le signal `timeout` toutes les 12 secondes pour faire défiler les astuces de la bannière.
  - **Minuteur à coup unique (`setSingleShot(True)`)** : Déclenche le signal `timeout` une seule fois après 3 200 ms pour faire disparaître le toast de succès (`setVisible(False)`).

### `PyQt6.QtCore.Qt`
- Énumérations standard : `Qt.Key.Key_Space`, `Qt.Key.Key_Comma` pour intercepter les touches du clavier ; `Qt.CursorShape.PointingHandCursor` pour afficher le pointeur main au survol.

---

## 2. Analyse Approfondie de la Classe `IpLineEdit`

Saisir des adresses IPv4 (comme `192.168.1.1`) dans un champ texte ordinaire est fastidieux : l'utilisateur doit constamment chercher la touche point `.` sur son pavé numérique ou son clavier AZERTY/QWERTY.

`IpLineEdit` hérite de `QLineEdit` et surcharge la méthode d'interception clavier **`keyPressEvent`** pour offrir une expérience de frappe fluide :

```python
class IpLineEdit(QLineEdit):
    def keyPressEvent(self, event):
        key = event.key()
        text = self.text()
        pos = self.cursorPosition()
```

### 2.1. Fonctionnalité 1 : La Barre d'Espace ou la Virgule insère un Point
```python
if key in (Qt.Key.Key_Space, Qt.Key.Key_Comma):
    if pos > 0 and text[pos - 1] not in ". ":
        if text.count(".") < 3:
            self.insert(".")
            return
    elif pos < len(text) and text[pos] == ".":
        self.setCursorPosition(pos + 1)
        return
    return
```
- Frapper la **Barre d'Espace** ou la **Virgule** insère automatiquement un point `.` si un chiffre a été tapé et qu'il n'y a pas déjà 3 points dans l'adresse.
- Si le curseur se trouve déjà juste devant un point existant, frapper Espace ou Virgule fait simplement franchir le point vers l'octet suivant (`setCursorPosition(pos + 1)`), évitant la duplication de points (`..`).

### 2.2. Fonctionnalité 2 : Appel du Comportement Standard
```python
super().keyPressEvent(event)
```
- Laisse le comportement normal de `QLineEdit` insérer le chiffre tapé et déplacer le curseur.

### 2.3. Fonctionnalité 3 : Algorithme "Smart Auto-Dot" (v1.2.0)
```python
if event.text().isdigit():
    cur_text = self.text()
    cur_pos = self.cursorPosition()
    if cur_pos == len(cur_text):
        last_dot = cur_text.rfind(".")
        last_space = cur_text.rfind(" ")
        sep = max(last_dot, last_space)
        octet = cur_text[sep + 1:] if sep != -1 else cur_text
        dots_count = cur_text.count(".") + cur_text.count(" ")

        if dots_count < 3 and octet.isdigit():
            val = int(octet)
            if len(octet) == 3 or (len(octet) == 2 and val >= 26):
                self.insert(".")
```
- **Détection des 3 chiffres** : Dès qu'un octet atteint 3 chiffres (ex: `192`), le point est inséré immédiatement.
- **Règle Prédictive des 2 chiffres $\ge 26$** :
  - *Raisonnement Mathématique Réseau* : Aucun octet IPv4 valide ne peut dépasser 255. Si l'utilisateur tape un nombre de 2 chiffres supérieur ou égal à 26 (ex: `32`, `99`, `68`), il est **mathématiquement impossible** qu'un 3ème chiffre s'y ajoute (car `320`, `990`, `680` dépassent tous 255).
  - L'application insère donc immédiatement le point après le 2ème chiffre, économisant une frappe à l'utilisateur !

---

## 3. Analyse de la Classe `MinecraftTipBanner`

```python
class MinecraftTipBanner(QFrame):
    def __init__(self, manager: TipsAndStreakManager, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.setObjectName("tipBanner")
        ...
        self.timer = QTimer(self)
        self.timer.setInterval(12000)
        self.timer.timeout.connect(lambda: self.advance_tip(randomize=False))
        self.timer.start()
```

- **Rôle** : Bandeau permanent en bas de la fenêtre affichant une astuce réseau ou ergonomique.
- **Interactivité** :
  - Défilement automatique toutes les 12 secondes.
  - Clic direct sur le texte du bandeau pour passer à l'astuce suivante (`mousePressEvent`).
  - Clic sur le bouton `🎲 Astuce` pour piocher une astuce au hasard (`advance_tip(randomize=True)`).

---

## 4. Analyse de la Classe `AdvancementToast`

```python
class AdvancementToast(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("advancementToast")
        self.setVisible(False)
        ...
        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.setInterval(3200)
        self.hide_timer.timeout.connect(lambda: self.setVisible(False))

    def show_advancement(self, adv: Advancement, streak: int):
        self.lbl_title.setText(f"🏆 Progrès débloqué : [{adv.title}]")
        self.lbl_desc.setText(f"{adv.description}  (🔥 Série : {streak})")
        self.setVisible(True)
        self.hide_timer.start()
```

- **Rôle** : Bannière dorée qui surgit en haut de l'interface lorsqu'un exercice est résolu avec succès sans aide.
- **Comportement Temporel** :
  - Lors du déclenchement, `setVisible(True)` affiche le bandeau et `self.hide_timer.start()` arme un compte à rebours de 3,2 secondes.
  - À l'expiration du délai, le slot `self.setVisible(False)` est exécuté sans perturber le travail de l'étudiant.
