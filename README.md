# 🌐 BitRoute — IPv4 Subnet, VLSM & Layer-3 Routing Toolkit (INPT ASEDS Edition)

A modular desktop application built with **Python** and **PyQt6** for mastering IPv4 addressing, binary-to-decimal octet conversion, subnetting, **VLSM**, **MTU fragmentation**, **Longest Prefix Match (LPM) routing**, and **16-bit IPv4 Header Checksums**.

---

## 📂 Repository Editions & Structure

| Directory | Edition / Platform | Description & Highlights |
| :--- | :--- | :--- |
| **[`./v1.2.0`](./v1.2.0)** | **v1.2.0 — Windows Edition** | Decoupled OOP architecture (`engine/` + `ui/`), 4 interactive training tabs (Binary & Mask Inspector, 32-Bit Subnet Practice, VLSM Express, Flash Drills), Minecraft-style streak & tip banner, and complete PDF/LaTeX manuals. |
| **[`./v1.2.0-linux`](./v1.2.0-linux)** | **v1.2.0 — Linux Edition** *(Fedora / RHEL / Ubuntu / Arch)* | Native Wayland/X11 desktop integration, Linux system typography (`Cantarell`, `JetBrains Mono`), 1-click PyInstaller build script (`build_linux.sh`), and GNOME `.desktop` application launcher installer. |
| **[`./v1.0.0`](./v1.0.0)** | **v1.0.0 — Classic Edition** | Original single-file standalone release (`converter.py`) with 8-Bit Binary Converter, Subnet Practice, and Hacker/Light themes. |

---

## ✨ What's New in v1.2.0

### 1. 🧱 Decoupled Modular Architecture (`engine/` vs `ui/`)
- **`engine/` (100% Pure Python, Zero UI Dependency)**: Built with clean Object-Oriented Programming (`@dataclass(frozen=True)` and pure static/class solvers) designed as a direct reference model for Java OOP porting (INPT ASEDS Engineering Curriculum).
- **`ui/` (PyQt6)**: Zero cognitive-overload interface built around the principle *"Test the decision, automate the repetition"*, featuring **☀️ Light Mode** and **💻 Hacker Dark (`#000000` / `#00FF66`)**.

### 2. 🧮 Tab 1 — 8-Bit Binary Converter & Mask Inspector
- **8 Interactive Bit Cards** (`128, 64, 32, 16, 8, 4, 2, 1`) with real-time **Binary / Decimal / Hexadecimal** synchronization.
- **Live Mask & Complement Inspector**:
  - Validates contiguous mask octets (`255, 254, 252, 248, 240, 224, 192, 128, 0`).
  - Computes **One's Complement (`~X = 255 - X`)** and **Subnet Step / Magic Number (`256 - X`)**.

### 3. 🎯 Tab 2 — Subnet Practice & 32-Bit Binary Drawer
- **Instant Classification Selectors**: `Class [A | B | C]` and `Type [Public | Private | APIPA | Loopback]`.
- **5-Row Subnet Table**: `Network`, `First Host`, `Last Host`, `Broadcast`, `Next Subnet`.
- **Progressive Disclosure 32-Bit Drawer**: Expandable panel showing `IP AND Mask`, `Internal Host ID (IP AND ~Mask)`, borrowed subnet bits ($2^{b_S}$), host bits ($2^{b_H} - 2$), plus course preset **`154.4.32.0/19`**.

### 4. 📐 Tab 3 — VLSM Express Workshop
- **Course Presets & Random Generator**: Includes official INPT course exercises (`193.225.34.0/24` with `[44, 20, 100]` and `192.168.0.0/24` with `[28, 4, 100]`).
- **Smart Auto-Completion**: Enter the sorted host requirement, `/CIDR`, and `Network Address` — once validated (`✓`), usable host ranges, broadcast, and decimal mask auto-complete automatically.

### 5. ⚡ Tab 4 — Flash Drills (MTU, LPM Routing & 16-Bit Checksum)
- **📦 MTU Fragmentation**: 8-byte payload alignment (`((MTU - IHL*4) // 8) * 8`), Fragment Offset (`/8`), and `MF (0/1)` flag.
- **🧭 Routing & Longest Prefix Match (LPM)**: 4-entry routing table testing *Longest Prefix Match*, *Administrative Distance* (`C=0, S=1, OSPF=110, RIP=120`), *Metric*, and *Default Route (`0.0.0.0/0`)*.
- **🧮 IPv4 Header Checksum (16-Bit)**: Hexadecimal sum, end-around carry folding, and final one's complement (`~Sum & 0xFFFF`).

### 6. 📚 Manuals & Code Walkthroughs
- **[Guide Application & Cours Réseau (PDF)](./v1.2.0/latex/01_Guide_Application_et_Cours_Reseau_v1.2.0.pdf)**
- **[Manuel Complet Learning IPv4 (PDF)](./v1.2.0/learning/Manuel_Complet_Learning_IPv4_v1.2.0.pdf)**
- **[14-Part Code Walkthrough (Markdown)](./v1.2.0/learning/code_walkthrough/README.md)**

---

## 🚀 Quick Start

### 🪟 Windows (`v1.2.0`)
```powershell
cd v1.2.0
pip install PyQt6
python bitroute.py
```
*(Or double-click `run_app.vbs` / `run_app.bat` inside `v1.2.0/` to launch without a console window).*

### 🐧 Linux (`v1.2.0-linux` — Fedora / Ubuntu / Arch)
**Option 1 — Build standalone native binary & desktop icon (Recommended):**
```bash
cd v1.2.0-linux
chmod +x build_linux.sh run_app.sh install_desktop_shortcut.sh
./build_linux.sh
./converter
```

**Option 2 — Run directly with Python:**
```bash
cd v1.2.0-linux
pip install PyQt6   # or: sudo dnf install -y python3-pyqt6
python3 converter.py
```

### 🏛️ Classic `v1.0.0`
```powershell
cd v1.0.0
pip install PyQt6
python bitroute.py
```
