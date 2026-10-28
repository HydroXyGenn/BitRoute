# 📚 Documentation LaTeX & Guides Pédagogiques — IPv4 Subnet Toolkit v1.2.0

Ce dossier regroupe les trois manuels PDF complets générés en LaTeX ainsi que leurs sources `.tex` et les captures d'écran haute résolution de l'application.

---

## 📄 Les 3 Manuels PDF

1. **[`01_Guide_Application_et_Cours_Reseau_v1.2.0.pdf`](./01_Guide_Application_et_Cours_Reseau_v1.2.0.pdf)** *(également dans `01_guide_application_et_cours/`)* :
   - **Rôle** : Guide visuel de l'application & Cours complet de Réseau IPv4 (INPT — Cursus Ingénieur ASEDS).
   - **Contenu** : 17 pages couvrant la philosophie ergonomique, 9 captures d'écran réelles, démonstrations mathématiques et corrigés des exercices officiels du cours (contiguïté, classes, VLSM, MTU, LPM, Checksum).

2. **[`02_Guide_Architecture_et_Code_v1.2.0.pdf`](./02_Guide_Architecture_et_Code_v1.2.0.pdf)** *(également dans `02_architecture_et_code/`)* :
   - **Rôle** : Revue de code, Architecture Logicielle (`engine/` vs `ui/`) & Blueprint de portage Java OOP.
   - **Contenu** : 13 pages couvrant le découplage Clean Architecture, le code Python/PyQt6 commenté, la gestion des entiers non signés et la compilation standalone.

3. **[`03_Manuel_Complet_Learning_v1.2.0.pdf`](./03_Manuel_Complet_Learning_v1.2.0.pdf)** *(également dans `03_manuel_learning_integral/` et dans `learning/`)* :
   - **Rôle** : Manuel intégral d'apprentissage et synthèse complète des 19 fichiers du dossier `learning/`.
   - **Contenu** : 37 pages couvrant les 6 parties du cursus :
     - Partie I : Architecture fondamentale & mathématiques réseau 8/32 bits.
     - Partie II : Algorithmes du cours INPT, presets officiels et solveurs (VLSM, MTU, LPM, Checksum).
     - Partie III : Gamification pédagogique, catalogue officiel des 16 astuces et système de trophées.
     - Partie IV : Ingénierie graphique PyQt6, `IpLineEdit` (Smart Auto-Dot), feuilles QSS unifiées et Zero Pixel Shift.
     - Partie V : Revue de code détaillée des 4 onglets spécialisés avec captures d'écran.
     - Partie VI : Cycle d'exécution système, compilation PyInstaller et blueprint de portage Java 17/21 OOP.

---

## 🗂️ Organisation du Dossier `latex/`

```text
latex/
├── README.md                                              # Ce fichier d'index
├── 01_Guide_Application_et_Cours_Reseau_v1.2.0.pdf        # PDF #1 : Guide de l'Application & Cours Réseau (17 pages)
├── 02_Guide_Architecture_et_Code_v1.2.0.pdf               # PDF #2 : Architecture Logicielle & Code Source (13 pages)
├── 03_Manuel_Complet_Learning_v1.2.0.pdf                  # PDF #3 : Manuel Intégral Learning Suite (37 pages)
├── 01_guide_application_et_cours/
│   ├── Guide_Application_et_Cours_Reseau_v1.2.0.tex       # Source LaTeX du PDF #1
│   └── Guide_Application_et_Cours_Reseau_v1.2.0.pdf       # PDF #1 compilé
├── 02_architecture_et_code/
│   ├── Guide_Architecture_et_Code_v1.2.0.tex              # Source LaTeX du PDF #2
│   └── Guide_Architecture_et_Code_v1.2.0.pdf              # PDF #2 compilé
├── 03_manuel_learning_integral/
│   ├── Manuel_Complet_Learning_IPv4_v1.2.0.tex            # Source LaTeX du PDF #3
│   └── Manuel_Complet_Learning_IPv4_v1.2.0.pdf            # PDF #3 compilé
└── screenshots/                                           # Captures d'écran haute résolution de la v1.2.0
    ├── 01_tab1_mask_valid_light.png
    ├── 02_tab1_mask_invalid_hacker.png
    ├── 03_tab2_subnet_solved_drawer_light.png
    ├── 04_tab2_subnet_hacker.png
    ├── 05_tab3_vlsm_cours1_solved_light.png
    ├── 06_tab3_vlsm_cours2_hacker.png
    ├── 07_tab4_drill_mtu_solved.png
    ├── 08_tab4_drill_lpm_solved.png
    └── 09_tab4_drill_checksum_solved.png
```
