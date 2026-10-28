# 📄 Guide de Fichier : `ui/tab_vlsm.py`

Le fichier [`ui/tab_vlsm.py`](file:///c:/Users/lenovo/Desktop/laformatik/ipv4-subnet-toolkit/v1.2.0/ui/tab_vlsm.py) implémente l'**Onglet 3 : Atelier VLSM Express — Décision Pure & Auto-Complétion**.

Ce module a été conçu pour éliminer la fatigue de calcul rébarbative tout en formant les étudiants aux véritables décisions d'ingénierie réseau : **le tri des besoins, le choix du masque `/CIDR` et le calcul de l'adresse réseau de départ**.

---

## 1. Philosophie Pédagogique : L'Anti-Saturation Cognitive

Dans les outils VLSM traditionnels, un étudiant doit remplir manuellement jusqu'à 7 colonnes par sous-réseau (Besoin, Masque décimal, Masque CIDR, Réseau, Premier hôte, Dernier hôte, Broadcast, Capacité utile). Sur un exercice de 4 sous-réseaux, cela représente 28 champs textes répétitifs qui épuisent l'étudiant sans lui apprendre de nouvelles notions de routage.

L'**Atelier VLSM Express** applique un principe d'**auto-complétion intelligente** :
- L'étudiant ne saisit que les **3 variables de décision fondamentales** :
  1. Le **Besoin trié** (vérifiant la règle du tri décroissant).
  2. Le **Préfixe `/CIDR`** (vérifiant la formule $2^h - 2 \ge N$).
  3. L'**Adresse Réseau** (vérifiant le calcul du pas / début de bloc).
- Dès que ces 3 valeurs sont correctes, l'application **auto-complète instantanément** la plage d'hôtes, le broadcast et le masque dans un badge vert émeraude (`autoSummaryBadge`) !

---

## 2. Bibliothèques et Modules Importés

```python
from typing import Callable, Dict, List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt

from engine.ipv4_math import IPv4MathEngine
from engine.vlsm_solver import VlsmProblem, VlsmSolver
from ui.widgets import IpLineEdit
```

- **`engine.vlsm_solver.VlsmSolver`** : Fournit les presets officiels du cours (`preset_cours_1`, `preset_cours_2`) et le générateur aléatoire `generate_random_problem`.
- **`ui.widgets.IpLineEdit`** : Champ réseau avec insertion rapide des points.

---

## 3. Structure Visuelle & Composants de l'Onglet

### 3.1. En-Tête & Énoncé du Problème (`#topBarContainer`)
- Affiche le réseau de départ (ex: `193.225.34.0/24`).
- Affiche les besoins en machines dans l'ordre non trié (ex: `44 , 20 , 100`).
- Boutons de chargement rapide :
  - `📘 Cours 1 (100, 44, 20)`
  - `📘 Cours 2 (100, 28, 4)`
  - `🎲 Nouveau VLSM` (générateur aléatoire de problèmes /24).

### 3.2. Tableau de Découpage à 3 Lignes (`#tableCard`)
Chaque ligne correspond à un sous-réseau à allouer et comporte :
1. **Libellé de Rang** : `SR #1 (1er besoin)`, `SR #2 (2ème besoin)`, `SR #3 (3ème besoin)`.
2. **Champ Besoin (N)** (`need_inputs`) : L'étudiant doit saisir la plus grande demande en premier (ex: `100`), puis la suivante (`44`), etc.
3. **Champ /CIDR** (`cidr_inputs`) : Préfixe calculé (ex: `/25`).
4. **Champ Adresse Réseau** (`net_inputs`) : Adresse de début du bloc (ex: `193.225.34.0`).
5. **Indicateur de Statut** : `✓` vert ou `✕` rouge.
6. **Badge d'Auto-Complétion** (`summary_badges`) :
   - Initialement : `🔒 Validez Besoin + /CIDR + Réseau...`
   - Une fois validé : `Plage: .1 → .126  |  Bcast: .127  |  Masque: .128`
7. **Bouton Aide (`Show`)** : Révèle la réponse de la ligne si besoin.

---

## 4. Analyse Technique du Code

### 4.1. Chargement d'un Problème : `_apply_problem(problem)`
```python
def _apply_problem(self, problem: VlsmProblem):
    self.current_problem = problem
    self.used_show_on_current = False
    self.rewarded_current = False
    self.row_shown = [False, False, False]

    self.lbl_base_net.setText(f"{problem.base_network_str}/{problem.base_cidr}")
    needs_str = " , ".join(str(n) for n in problem.unsorted_needs)
    self.lbl_unsorted_needs.setText(needs_str)

    for i in range(3):
        for widget in (self.need_inputs[i], self.cidr_inputs[i], self.net_inputs[i]):
            widget.blockSignals(True)
            widget.clear()
            widget.blockSignals(False)
        self._update_row_visuals(i, is_valid=False)
        self.show_buttons[i].setText("Show")
```
- **L'Astuce `blockSignals(True)`** : Lors de la réinitialisation des champs, bloquer temporairement les signaux empêche le déclenchement intempestif des méthodes de validation sur des champs à moitié effacés.

### 4.2. Validation d'une Ligne : `validate_row(row_idx: int)`
```python
def validate_row(self, row_idx: int):
    if self.current_problem is None:
        return
    alloc = self.current_problem.allocations[row_idx]

    need_txt = self.need_inputs[row_idx].text().strip()
    need_ok = need_txt.isdigit() and int(need_txt) == alloc.hosts_needed

    cidr_val = self._parse_cidr(self.cidr_inputs[row_idx].text())
    cidr_ok = (cidr_val == alloc.cidr)

    net_norm = IPv4MathEngine.normalize_ip_input(self.net_inputs[row_idx].text())
    net_ok = (net_norm == alloc.network_str)

    is_valid = need_ok and cidr_ok and net_ok
    self._update_row_visuals(row_idx, is_valid=is_valid)
    self._check_all_solved()
```
- Vérifie simultanément que :
  1. Le besoin correspond au rang trié de la solution (`hosts_needed`).
  2. Le masque `/CIDR` correspond exactement au préfixe minimal requis.
  3. L'adresse réseau démarre au bon bloc.

### 4.3. Révélation du Badge d'Auto-Complétion : `_update_row_visuals()`
```python
def _update_row_visuals(self, row_idx: int, is_valid: bool):
    lbl_st = self.status_labels[row_idx]
    badge = self.summary_badges[row_idx]
    alloc = self.current_problem.allocations[row_idx]

    if is_valid:
        lbl_st.setText("✓")
        lbl_st.setObjectName("statusCorrect")
        badge.setText(alloc.last_octet_summary)
        badge.setProperty("solved", True)
    else:
        lbl_st.setText("✕")
        lbl_st.setObjectName("statusWrong")
        badge.setText("🔒 Validez Besoin + /CIDR + Réseau...")
        badge.setProperty("solved", False)

    lbl_st.style().unpolish(lbl_st)
    lbl_st.style().polish(lbl_st)
    badge.style().unpolish(badge)
    badge.style().polish(badge)
```
- Dès que `is_valid` passe à `True`, le badge affiche la propriété `alloc.last_octet_summary` et passe en vert (`[solved="true"]`).

### 4.4. Déblocage du Succès : `_check_all_solved()`
- Si les 3 lignes affichent `✓` et qu'aucun bouton *"Show"* n'a été utilisé, la fonction déclenche `on_clean_solve("vlsm_clean")`, octroyant le succès **"Architecte VLSM"** et augmentant la série active.
