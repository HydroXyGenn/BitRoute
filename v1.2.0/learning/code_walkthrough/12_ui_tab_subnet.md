# 📄 Guide de Fichier : `ui/tab_subnet.py`

Le fichier [`ui/tab_subnet.py`](file:///c:/Users/lenovo/Desktop/laformatik/ipv4-subnet-toolkit/v1.2.0/ui/tab_subnet.py) implémente l'**Onglet 2 : Pratique du Sous-Réseau, Sélecteurs Classe/Portée & Tiroir Binaire 32 Bits**.

C'est l'écran d'entraînement principal à l'adressage IPv4 et au découpage en sous-réseaux, intégrant l'exemple officiel du cours de l'INPT (`154.4.32.0/19`).

---

## 1. Rôle dans l'Architecture

L'onglet 2 est structuré selon le principe de **Divulgation Progressive (Progressive Disclosure)** :
- Au départ, l'écran ne présente que les questions nécessaires : l'adresse IP cible avec son CIDR, les boutons de classification (Classe et Type), et les 5 champs classiques d'examen (Adresse Réseau, Premier Hôte, Dernier Hôte, Diffusion Broadcast, Sous-réseau suivant).
- Si l'étudiant hésite ou commet une erreur, il peut dérouler le **Tiroir Binaire 32 bits**, qui décompose l'opération logique bit à bit pour lui faire comprendre pourquoi son calcul a échoué.

---

## 2. Bibliothèques et Modules Importés

```python
from typing import Callable, Dict, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QFrame
)
from PyQt6.QtCore import Qt

from engine.ipv4_math import IPv4MathEngine, SubnetAnalysis
from ui.widgets import IpLineEdit
```

- **`engine.ipv4_math.IPv4MathEngine`** : Génère les problèmes aléatoires équilibrés (`generate_practice_problem`) et résout l'exemple du cours (`analyze_subnet("154.4.32.0", 19)`).
- **`ui.widgets.IpLineEdit`** : Permet la saisie rapide des adresses IP avec insertion automatique des points via barre d'espace ou virgule.
- **`Callable[[str], None]`** : Typage du callback de streak transmis par `MainWindow`.

---

## 3. Structure Visuelle & Composants de l'Onglet

L'écran comporte 4 sections :

### 3.1. Bandeau Supérieur (`#topBarContainer`)
- Affiche l'adresse IP cible (ex: `154 . 4 . 32 . 0`) et son préfixe `/CIDR` (ex: `19`).
- Bouton `📘 Ex. Cours (154.4.32.0/19)` : Charge instantanément l'exercice canonique de l'INPT.
- Bouton `Next Problem` : Génère un nouveau problème aléatoire.

### 3.2. Sélecteurs Rapides Classe & Portée (`#headerCard`)
- **Classe** : Boutons `A`, `B`, `C` avec indicateur `✓` ou `✕`.
- **Type** : Boutons `Publique`, `Privée`, `APIPA`, `Loopback` avec indicateur `✓` ou `✕`.
- Dès que l'étudiant clique, la réponse est validée instantanément.

### 3.3. Tableau Principal des 5 Lignes (`#tableCard`)
Grille de 5 lignes comprenant :
1. **Network** (Adresse Réseau)
2. **First Host** (Premier Hôte Utilisable)
3. **Last Host** (Dernier Hôte Utilisable)
4. **Broadcast** (Adresse de Diffusion)
5. **Next Subnet** (Sous-Réseau Suivant)

Chaque ligne dispose de :
- Un champ de saisie `IpLineEdit`.
- Un indicateur de correction dynamique (`✓` vert ou `✕` rouge).
- Un champ masqué de réponse (`answer_fields`).
- Un bouton `Show` permettant d'afficher la réponse si l'élève est bloqué.

### 3.4. Tiroir Binaire 32 Bits (`#drawerCard`)
- Masqué par défaut (`setVisible(False)`).
- Accessible via le bouton bascule `🔍 Afficher le détail binaire (32 bits)`.
- Affiche l'opération bit à bit complète :
  ```
  IP Cible       (154.4.32.0   ) : 10011010.00000100.00100000.00000000
  Masque /19     (255.255.224.0) : 11111111.11111111.11100000.00000000
  IP ET Masque   (Network      ) : 10011010.00000100.00100000.00000000
  IP ET ~Masque  (Host ID      ) : 00000000.00000000.00000000.00000000
  • Classe B (bits 10..., masque par défaut /16) | Portée : Publique
  • Bits empruntés : b_S = 19 - 16 = 3 bits -> 2^3 = 8 sous-réseaux
  • Bits d'hôtes   : b_H = 32 - 19 = 13 bits -> 2^13 - 2 = 8190 hôtes
  ```

---

## 4. Analyse Technique du Code

### 4.1. Chargement d'un Problème : `_apply_problem(analysis)`
```python
def _apply_problem(self, analysis: SubnetAnalysis):
    self.current_analysis = analysis
    self.used_show_on_current = False
    self.rewarded_current = False

    self.answers = {
        "Network": analysis.network_str,
        "First Host": analysis.first_host_str,
        "Last Host": analysis.last_host_str,
        "Broadcast": analysis.broadcast_str,
        "Next Subnet": analysis.next_subnet_str,
    }
```
- Réinitialise les drapeaux de streak (`used_show_on_current = False`, `rewarded_current = False`).
- Stocke les réponses exactes calculées par le moteur.
- Vide les champs de saisie, remet les statuts à `✕` et masque les réponses.
- Met à jour le texte du tiroir binaire avec les explications détaillées.

### 4.2. Validation en Direct : `validate_input(key: str)`
```python
def validate_input(self, key: str):
    if self.current_analysis is None:
        return
    expected = self.answers.get(key, "")
    user_val = IPv4MathEngine.normalize_ip_input(self.input_fields[key].text())
    is_correct = (user_val == expected)

    lbl = self.status_labels[key]
    if is_correct:
        lbl.setText("✓")
        lbl.setObjectName("statusCorrect")
    else:
        lbl.setText("✕")
        lbl.setObjectName("statusWrong")
    lbl.style().unpolish(lbl)
    lbl.style().polish(lbl)

    self._check_all_solved()
```
- Grâce au signal `textChanged` de chaque `IpLineEdit`, la validation s'exécute **à chaque caractère tapé**.
- `IPv4MathEngine.normalize_ip_input` élimine les zéros non significatifs ou espaces pour comparer rigoureusement des adresses IPv4 identiques.

### 4.3. Attribution du Succès : `_check_all_solved()`
```python
def _check_all_solved(self):
    if self.rewarded_current or self.used_show_on_current:
        return
    all_rows = all(self.status_labels[k].text() == "✓" for k in self.row_keys)
    class_ok = (self.lbl_class_status.text() == "✓")
    type_ok = (self.lbl_type_status.text() == "✓")

    if all_rows and class_ok and type_ok:
        self.rewarded_current = True
        if self.on_clean_solve:
            self.on_clean_solve("subnet_clean")
```
- Si l'étudiant a trouvé la classe, le type et les 5 adresses sans avoir cliqué une seule fois sur *"Show"*, le callback `on_clean_solve("subnet_clean")` est invoqué, déclenchant l'incrémentation de la série et le trophée **"Maître du Masque"**.
