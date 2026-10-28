# 📄 Guide de Fichier : `ui/themes.py`

Le fichier [`ui/themes.py`](file:///c:/Users/lenovo/Desktop/laformatik/ipv4-subnet-toolkit/v1.2.0/ui/themes.py) définit les deux signatures visuelles de l'application via des feuilles de style **QSS (Qt Style Sheets)** :
1. **Modern Light Mode** : Palette épurée ardoise/bleu royaux (`#F4F7FB`, `#1E40AF`, `#2563EB`).
2. **Hacker Console Dark Mode** : Noir absolu (`#000000`) et vert phosphore terminal (`#00FF66`).

Ce module a été rigoureusement calibré pour garantir un **déplacement de 0 pixel (Zero Layout Shift)** lors du basculement d'un thème à l'autre.

---

## 1. Fonctionnement des Feuilles de Style QSS en PyQt6

### 1.1. Qu'est-ce que le QSS ?
Qt Style Sheets (QSS) est un puissant mécanisme déclaratif inspiré du CSS du Web, permettant de personnaliser l'apparence des composants natifs Qt :
- **Sélecteurs de type** : Ciblent une classe Qt (ex: `QMainWindow`, `QTabWidget::pane`, `QTabBar::tab`).
- **Sélecteurs d'identifiant (`#objectName`)** : Ciblent un composant précis ayant défini `.setObjectName("monNom")` (ex: `#btnThemeToggle`, `#bitBox`, `#syncInput`).
- **Pseudo-états (`:hover`, `:pressed`, `:checked`, `:focus`)** : Réagissent aux interactions utilisateur.
- **Sélecteurs de propriétés dynamiques (`[active="true"]`, `[solved="true"]`)** : Modifient le style en temps réel sans recharger l'interface lorsque le code Python appelle `widget.setProperty("active", True)`.

---

## 2. Le Défi du "Zero Pixel Shift" (Résolu en v1.2.0)

Lorsqu'on bascule d'un thème clair vers un thème sombre, si les propriétés qui composent la boîte de calcul de taille (**Box Model**) diffèrent, la fenêtre subit un décalage visuel désagréable (*layout shift*) :
- Des boutons bougent de quelques pixels.
- La barre d'onglets s'élargit et fait apparaître des flèches de défilement horizontal `< >`.

### Règles d'or unifiées dans `themes.py` :
| Propriété Box Model | Thème Clair (`get_light_qss`) | Thème Hacker (`get_dark_qss`) | Résultat |
|:---|:---|:---|:---|
| **`font-family` (Global UI)** | `'Segoe UI', sans-serif` | `'Segoe UI', sans-serif` | Même largeur de glyphe pour les onglets et libellés. |
| **`font-family` (Technique)** | `'Consolas', monospace` | `'Consolas', monospace` | Adresses IP et masques à espacement constant. |
| **`font-size` & `font-weight`** | `13px` / `600` | `13px` / `600` | Zéro variation d'épaisseur de texte sur les onglets. |
| **`border-width` structurel** | `1.5px solid` | `1.5px solid` | Zéro variation de marge intérieure/extérieure. |
| **`padding` des onglets** | `8px 14px` | `8px 14px` | Dimensions de rectangles d'onglets 100 % identiques. |

---

## 3. Analyse Détaillée des Sélecteurs QSS

### 3.1. Structure Générale & Onglets (`QTabWidget`, `QTabBar::tab`)
```css
QTabWidget::pane {
    border: 1.5px solid #E2E8F0;  /* Vert foncé #00551A en mode sombre */
    background: #F8FAFC;          /* Noir #020702 en mode sombre */
    border-top: none;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
}

QTabBar::tab {
    font-weight: 600;
    font-size: 13px;
    padding: 8px 14px;
    margin-right: 4px;
    border: 1.5px solid #CBD5E1;
    border-bottom: none;
}

QTabBar::tab:selected {
    border-top: 3px solid #2563EB;  /* Bordure supérieure d'accentuation */
}
```
- **Rôle** : Crée des onglets arrondis sur le dessus avec un indicateur visuel net (`border-top: 3px solid`) signalant l'onglet actif.

### 3.2. Cartes de Conteneur (`#headerCard`, `#mainCard`, `#tableCard`, `#inspectorCard`)
```css
#headerCard, #mainCard, #tableCard, #inspectorCard, #drawerCard {
    background-color: #FFFFFF;    /* Sombre: #040A04 */
    border: 1.5px solid #E2E8F0;  /* Sombre: #00551A */
    border-radius: 12px;
}
```
- **Rôle** : Regroupe les contrôles dans des "cartes" (Cards) modernes aux coins arrondis de 12px, séparant distinctement les blocs d'information.

### 3.3. Contrôles Interactifs de Bits (`#bitBox`, `QCheckBox#bitCheckBox`)
```css
#bitBox {
    background-color: #F8FAFC;
    border: 1.5px solid #CBD5E1;
    border-radius: 10px;
}

#bitBox[active="true"] {
    background-color: #EFF6FF;    /* Vert néon subtil en sombre: #00220A */
    border: 2px solid #3B82F6;     /* Vert néon éclatant en sombre: #00FF66 */
}

QCheckBox#bitCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 6px;
}
```
- **Rôle** : Dans l'Onglet 1 (Convertisseur 8-bit), chaque bit possède sa carte dédiée. Le sélecteur de propriété `[active="true"]` illumine instantanément la carte dès que la case à cocher correspondante passe à `1`.

### 3.4. Champs d'Entrée Monospace (`#syncInput`, `#subnetInput`)
```css
#syncInput, #subnetInput {
    border: 1.5px solid #94A3B8;
    border-radius: 8px;
    padding: 5px 10px;
    font-size: 15px;
    font-weight: 700;
    font-family: 'Consolas', 'Courier New', monospace;
}

#syncInput:focus, #subnetInput:focus {
    border: 2px solid #2563EB;     /* Focus bleu ou vert néon */
}
```
- **Rôle** : Les adresses IP et nombres binaires exigent une police à chasse fixe (`Consolas`) afin que les chiffres et les points s'alignent parfaitement sur des colonnes verticales régulières.

### 3.5. Indicateurs de Validation & Badges (`#statusCorrect`, `#statusWrong`, `#autoSummaryBadge`)
```css
#statusCorrect {
    font-size: 16px;
    font-weight: 900;
    color: #16A34A; /* Vert validation */
}

#statusWrong {
    font-size: 16px;
    font-weight: 900;
    color: #DC2626; /* Rouge correction */
}

#autoSummaryBadge[solved="true"] {
    border: 1.5px solid #22C55E;
    color: #15803D;
    background-color: #F0FDF4;
}
```
- **Rôle** : Fournit un retour visuel immédiat (Feedback Loop) à l'étudiant dès qu'il saisit une valeur correcte ou incorrecte.

---

## 4. Les Deux Fonctions Publiques

1. **`get_light_qss() -> str`** : Retourne la chaîne QSS complète pour le thème clair.
2. **`get_dark_qss() -> str`** : Retourne la chaîne QSS complète pour le thème Hacker Dark.

Ces fonctions sont appelées par la méthode `apply_theme()` de `MainWindow` lors du basculement via le bouton `#btnThemeToggle`.
