# 📄 Guide de Fichier : `ui/__init__.py`

Le fichier [`ui/__init__.py`](file:///c:/Users/lenovo/Desktop/laformatik/ipv4-subnet-toolkit/v1.2.0/ui/__init__.py) transforme le répertoire `ui/` en un paquetage Python et expose le composant principal d'interface.

---

## 1. Rôle dans l'Architecture

De manière symétrique à `engine/__init__.py`, le paquetage `ui/` encapsule l'ensemble des modules graphiques :
- Les widgets sur-mesure (`widgets.py`).
- Les feuilles de style unifiées (`themes.py`).
- Les 4 onglets interactifs (`tab_binary.py`, `tab_subnet.py`, `tab_vlsm.py`, `tab_drills.py`).
- La fenêtre principale orchestratrice (`main_window.py`).

`ui/__init__.py` expose **uniquement** [`MainWindow`](file:///c:/Users/lenovo/Desktop/laformatik/ipv4-subnet-toolkit/v1.2.0/ui/main_window.py) au reste du programme, préservant ainsi le principe d'encapsulation.

---

## 2. Code Source et Analyse

```python
"""
IPv4 Subnet Toolkit v1.2.0 — PyQt6 User Interface Package
"""

from .main_window import MainWindow

__all__ = ["MainWindow"]
```

### 2.1. L'Import Relatif `from .main_window import MainWindow`
- Permet au point d'entrée [`converter.py`](file:///c:/Users/lenovo/Desktop/laformatik/ipv4-subnet-toolkit/v1.2.0/converter.py) d'importer directement :
  ```python
  from ui.main_window import MainWindow
  ```
  ou encore :
  ```python
  from ui import MainWindow
  ```
- Les détails d'implémentation des onglets et des widgets restent cachés à l'intérieur du paquetage `ui/`.

### 2.2. La Liste `__all__ = ["MainWindow"]`
- Indique formellement aux linters statiques et à l'interpréteur que la seule classe publique du paquetage pour le point d'entrée est `MainWindow`.
