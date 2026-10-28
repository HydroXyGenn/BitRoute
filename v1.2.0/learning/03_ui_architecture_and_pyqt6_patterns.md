# 03 — Ingénierie de l'Interface PyQt6 & Ergonomie Anti-Saturation (`ui/`)

Ce document explique les patterns de programmation **PyQt6**, la gestion des événements clavier, le système de feuilles de style dynamiques **QSS** et les choix ergonomiques implémentés dans le dossier `ui/` de **IPv4 Subnet Toolkit v1.2.0**.

---

## 1. Saisie Clavier Ultra-Rapide : `IpLineEdit` (`ui/widgets.py`)

### 1.1. Surcharge de `keyPressEvent(self, event)`
Dans `PyQt6`, chaque touche pressée dans un `QLineEdit` déclenche `keyPressEvent(QKeyEvent)`.
Notre widget personnalisé `IpLineEdit` hérite de `QLineEdit` et intercepte l'événement en deux temps :

1. **Avant `super().keyPressEvent(event)` (Interception de l'Espace et de la Virgule)** :
   - Si l'utilisateur appuie sur `Espace` ou `,`, au lieu d'écrire un espace, on vérifie que le caractère précédent n'est pas déjà un point et qu'il y a moins de 3 points dans le champ (`text.count(".") < 3`), puis on appelle `self.insert(".")`.
   - Si le curseur se trouve juste devant un `.` existant, `Espace` déplace simplement le curseur après le point.
2. **Après `super().keyPressEvent(event)` (Lookahead mathématique Auto-Dot)** :
   - Dès qu'un chiffre est tapé à la fin du champ, on extrait l'octet en cours de saisie (après le dernier `.`).
   - **Règle des 3 chiffres** : Si `len(octet) == 3` (ex: `192`), l'octet est complet $\rightarrow$ on insère `.`.
   - **Règle v1.2.0 (`int(octet) >= 26` dès 2 chiffres)** : La valeur maximale d'un octet IPv4 est `255`. Par conséquent, **aucun octet valide à 3 chiffres ne peut commencer par `26` à `99`** (car $260 > 255$). Dès que l'utilisateur tape 2 chiffres dont la valeur est $\ge 26$ (ex: `32`, `68`, `99`), `IpLineEdit` insère immédiatement le `.` sans attendre !

---

## 2. Sélecteurs Dynamiques QSS & Rafraîchissement (`unpolish` / `polish`)

### 2.1. Propriétés dynamiques Qt (`setProperty`)
Au lieu de coder en dur des couleurs Python avec `setStyleSheet(...)` sur chaque bouton (ce qui casserait le changement de thème Light / Hacker Dark), nous utilisons les **sélecteurs d'attributs QSS** dans `ui/themes.py` :
- `#bitBox[active="true"]` : Carte de bit allumée dans l'onglet 1.
- `#choiceBtn[selected="true"]` : Bouton de sélection actif (Classe A/B/C, Type, Route #1..#4, Règle LPM).
- `#drillNavBtn[active="true"]` : Onglet de navigation du mini-exercice actif dans l'onglet 4.
- `#autoSummaryBadge[solved="true"]` : Bandeau de résumé VLSM déverrouillé en vert dès que la ligne est valide.

### 2.2. Pourquoi appeler `unpolish()` puis `polish()` ?
Dans Qt, modifier une propriété dynamique avec `widget.setProperty("active", True)` ne recalcule pas automatiquement le style CSS pour des raisons de performance. Il faut notifier le moteur de style :
```python
widget.setProperty("active", is_on)
widget.style().unpolish(widget)
widget.style().polish(widget)
```
Cette idiome garantit que le widget adopte instantanément les couleurs du thème courant (Bleu en Light Mode, Vert phosphore `#00FF66` en Hacker Dark Mode).

---

## 3. Verrou Anti-Boucle Infinie (`self._updating`) dans l'Onglet 1

Dans `BinaryConverterTab` (`ui/tab_binary.py`), 4 composants modifient la même valeur (`0..255`) :
- Les 8 cases à cocher (`stateChanged`)
- Le champ Binaire (`textEdited`)
- Le champ Décimal (`textEdited`)
- Le champ Hexadécimal (`textEdited`)

Pour éviter toute récursion infinie lorsqu'un composant met à jour les autres, la méthode centrale `apply_value(self, val: int, source: str)` utilise un drapeau `self._updating = True` dans un bloc `try ... finally` et ne réécrit pas dans le champ `source` que l'utilisateur est en train d'éditer (afin de ne pas déplacer son curseur pendant la frappe).

---

## 4. Ergonomie Cognitive : Divulgation Progressive & Auto-Complétion

1. **Divulgation Progressive (Onglet 2 — `SubnetPracticeTab`)** :
   - Le tiroir binaire 32 bits (`self.drawer_card`) est masqué par défaut (`setVisible(False)`).
   - **Subtilité Qt (`isHidden()` vs `isVisible()`)** : Dans un `QTabWidget`, `widget.isVisible()` retourne `False` si l'onglet parent n'est pas l'onglet actuellement affiché à l'écran. En revanche, `widget.isHidden()` vérifie l'état propre du widget indépendamment de la visibilité de son parent. Utiliser `vis = self.drawer_card.isHidden()` dans `toggle_binary_drawer()` garantit un comportement fiable aussi bien au clic utilisateur que lors des tests automatisés.
   - L'utilisateur se concentre d'abord sur le calcul mental rapide (avec le *Magic Number*), puis clique sur `🔍 Afficher le détail binaire (32 bits)` s'il souhaite visualiser l'alignement bit à bit de `IP ET Masque` et `IP ET ~Masque`.
2. **Auto-Complétion Anti-Répétition (Onglet 3 — `VlsmLabTab`)** :
   - Dès que `validate_row(row_idx)` confirme que `(Besoin, /CIDR, Network IP)` sont exacts, la colonne de résumé passe de l'état verrouillé (`🔒`) à l'état résolu (`solved="true"`) et affiche la plage d'hôtes, le Broadcast et le masque sans demander 12 saisies supplémentaires.
3. **Navigation par Pile (`QStackedWidget` dans l'Onglet 4 — `FlashDrillsTab`)** :
   - Au lieu d'empiler 3 exercices denses sur un seul écran, `QStackedWidget` n'affiche qu'une seule vue à la fois (`MTU`, `Routage LPM` ou `Checksum Hexa`), gardant l'interface aérée.

---

## 5. Gamification & Timers Asynchrones (`QTimer`)

- **`MinecraftTipBanner`** : Utilise un `QTimer` périodique (`setInterval(12000)`) connecté à `advance_tip()` pour faire défiler automatiquement les 16 astuces du cours INPT et raccourcis sans bloquer le thread principal (Event Loop Qt).
- **`AdvancementToast` & Système de Série (`🔥 Série : X`)** :
  - Chaque onglet d'exercice maintient deux booléens par problème : `used_show_on_current` et `rewarded_current`.
  - Si l'utilisateur clique sur `Show`, `used_show_on_current` passe à `True` (pas de gain de série sur cet exercice).
  - Si toutes les conditions de l'exercice sont validées (`✓`) avec `used_show_on_current == False`, l'onglet invoque le callback `on_clean_solve(category_key)` fourni par `MainWindow`, qui incrémente la série et déclenche le `QTimer` *single-shot* de 3,2 secondes de `AdvancementToast`.
