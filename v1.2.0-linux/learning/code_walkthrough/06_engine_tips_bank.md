# 📄 Guide de Fichier : `engine/tips_bank.py`

Le fichier [`engine/tips_bank.py`](file:///c:/Users/lenovo/Desktop/laformatik/ipv4-subnet-toolkit/v1.2.0/engine/tips_bank.py) implémente le moteur de **gamification pédagogique**, la banque rotative d'astuces façon Minecraft et le gestionnaire de séries de victoires (*Streak Counter* & *Advancements*).

Comme tous les modules de `engine/`, il fonctionne sans aucune dépendance graphique.

---

## 1. Rôle dans l'Architecture

La gamification transforme un outil d'apprentissage austère en une expérience stimulante :
1. **Pédagogie Passive** : Une bannière tournante en bas de l'écran distille en continu les règles clés du cours INPT et les raccourcis ergonomiques de l'application.
2. **Renforcement Positif** : Récompenser l'étudiant qui résout un exercice par lui-même sans utiliser le bouton d'aide *"Show"* par une incrémentation de flamme (`🔥 Série : N`) et des succès débloqués (*Toast Advancements*).

---

## 2. Bibliothèques et Modules Importés

```python
from dataclasses import dataclass
import random
from typing import Dict, List, Optional, Set
```

- **`dataclass(frozen=True)`** : Modélise les entrées immuables `TipEntry` et `Advancement`.
- **`random`** : Utilisé pour tirer aléatoirement une astuce lors du clic sur le dé (`🎲 Astuce`).
- **`Set[str]`** : Utilisé pour stocker les clés uniques des succès débloqués (`unlocked_keys`), assurant des recherches d'appartenance instantanées en $\mathcal{O}(1)$.

---

## 3. Modèles de Données & Catalogue

### 3.1. `@dataclass(frozen=True) class TipEntry`
```python
@dataclass(frozen=True)
class TipEntry:
    category: str   # "[⚡ APP TIP]", "[🧠 COURS INPT]", "[🔥 ASTUCE PRO]"
    text: str

    @property
    def formatted(self) -> str:
        return f"{self.category}  {self.text}"
```

### 3.2. Catalogue `TIPS_LIST` (16 Astuces Réseau & Ergonomie)
Le catalogue couvre trois piliers d'apprentissage :
1. **`[⚡ APP TIP]` (Ergonomie & Productivité)** :
   - Insertion instantanée de point via barre d'espace ou virgule.
   - Smart Auto-Dot : saisie de 2 chiffres $\ge 26$ ajoutant automatiquement le point.
2. **`[🧠 COURS INPT]` (Formules Fondamentales)** :
   - Les 9 octets de masque contigus valides.
   - Règle d'or du tri décroissant VLSM et formule $2^h - 2 \ge N$.
   - Fragmentation IPv4 (IHL $\times 4$, charge utile multiple de 8, offset).
   - Décision de routage (LPM $\to$ AD $\to$ Métrique $\to$ Route par défaut).
   - Checksum 16 bits (addition, end-around carry et inversion).
3. **`[🔥 ASTUCE PRO]` (Raccourcis de Calcul Mental)** :
   - Formule du Magic Number ($256 - \text{Masque}$).
   - Calcul de l'Host ID interne par $\text{IP} \ \& \ (\sim\text{Masque})$.

### 3.3. Catalogue `ADVANCEMENTS_CATALOG`
Définit les succès inspirés des trophées Minecraft :
- `"subnet_clean"` : **Maître du Masque** (Sous-réseau résolu sans aide).
- `"vlsm_clean"` : **Architecte VLSM** (Découpage sans gaspillage).
- `"mtu_clean"` : **Chirurgien MTU** (Fragmentation au multiple de 8 près).
- `"lpm_clean"` : **Routeur Humain** (Règle LPM/AD maîtrisée).
- `"checksum_clean"` : **Seigneur du Checksum** (Checksum parfait).
- `"streak_3"` : **Série de 3 (On Fire 🔥)** (3 victoires consécutives).
- `"streak_5"` : **Ingénieur Réseau INPT** (5 victoires consécutives).

---

## 4. Analyse de la Classe `TipsAndStreakManager`

Cette classe maintient l'état applicatif de la progression de l'étudiant.

### 4.1. Constructeur `__init__()`
```python
def __init__(self) -> None:
    self.tips: List[TipEntry] = list(TIPS_LIST)
    self._tip_index: int = 0
    self.streak: int = 0
    self.unlocked_keys: Set[str] = set()
```
- Initialise la liste des astuces, l'index de départ, le compteur de streak à 0, et l'ensemble vide des succès obtenus.

### 4.2. Navigation dans les Astuces : `next_tip(randomize)`
```python
def next_tip(self, randomize: bool = False) -> TipEntry:
    if randomize:
        self._tip_index = random.randrange(len(self.tips))
    else:
        self._tip_index = (self._tip_index + 1) % len(self.tips)
    return self.tips[self._tip_index]
```
- **Mode Séquentiel** (`randomize=False`) : Utilise l'opérateur modulo `% len(self.tips)` pour boucler indéfiniment de manière circulaire.
- **Mode Aléatoire** (`randomize=True`) : Tire un index équiprobable via `random.randrange()`.

### 4.3. Enregistrement d'un Succès : `record_clean_solve(category_key)`
```python
def record_clean_solve(self, category_key: str) -> Optional[Advancement]:
    self.streak += 1

    # Vérification prioritaire des paliers de série
    if self.streak == 5 and "streak_5" not in self.unlocked_keys:
        self.unlocked_keys.add("streak_5")
        return ADVANCEMENTS_CATALOG["streak_5"]
    if self.streak == 3 and "streak_3" not in self.unlocked_keys:
        self.unlocked_keys.add("streak_3")
        return ADVANCEMENTS_CATALOG["streak_3"]

    adv = ADVANCEMENTS_CATALOG.get(category_key)
    if adv is not None:
        self.unlocked_keys.add(category_key)
        return adv
    return None
```
- Incrémente la série active.
- Priorise les trophées d'endurance (`streak_3`, `streak_5`).
- Retourne l'objet `Advancement` pour que l'interface puisse afficher la bannière temporisée (`AdvancementToast`), ou `None` si aucun trophée particulier n'est débloqué.

### 4.4. Réinitialisation : `reset_streak()`
- Remet le compteur de série à zéro si l'utilisateur abandonne et clique sur le bouton d'aide *"Show"*.
