# 🌐 IPv4 Binary Converter & Subnet Practice Toolkit

A modern desktop application built with **Python** and **PyQt6** for mastering IPv4 networking fundamentals, binary-to-decimal octet conversion, and subnetting practice.

---

## ✨ Features

### 1. 🧮 8-Bit Binary Converter
- **8 Interactive Bit Toggles**: Checkboxes for bit values (`128, 64, 32, 16, 8, 4, 2, 1`).
- **3-Way Real-Time Live Sync**:
  - Type directly into **Binary (8-bit)** (`10101010`).
  - Type into **Decimal (0 - 255)** (`170`).
  - Type into **Hexadecimal (00 - FF)** (`0xAA`).
  - Toggle checkboxes to automatically synchronize all formats simultaneously.
- **Quick Presets**: `All 1s (255)`, `Clear All (0)`, and `Invert Bits`.

### 2. 🎯 Subnet Practice
- **Random Target Generation**: Generates random IPv4 addresses with CIDR prefixes (`/8` to `/30`).
- **Network Calculations**:
  - `Network Address`
  - `First Usable Host`
  - `Last Usable Host`
  - `Broadcast Address`
  - `Next Subnet`
- **Instant Validation**: Real-time feedback changing dynamically from `✕` to `✓`.
- **Effortless IP Typing**:
  - Supports typing with simple spaces (e.g., `222 80 61 0`).
  - Spacebar automatically inputs dots.
  - Automatically advances after 3 digits.
- **Answer Reveal**: Toggleable `Show`/`Hide` buttons to view solutions.

### 3. ⚡ Themes
- **💻 Hacker Console**: Ultra-cool Matrix black (`#000000`) and phosphor neon green (`#00FF66`) theme with monospace typography.
- **☀️ Light Mode**: Modern clean theme with soft blue accents.
- 1-click theme switcher in the top-right corner.

---

## 🚀 How to Run

### Option 1: Standalone `.exe` (No Python Required)
Run `converter.exe` directly, or double-click `run_app.vbs` to launch silently without any terminal window.

### Option 2: From Source
1. Install Python 3.10+
2. Install dependencies:
   ```bash
   pip install PyQt6
   ```
3. Run the application:
   ```bash
   python converter.py
   ```

---

## 🛠 Compiling to `.exe`
To rebuild the standalone executable with PyInstaller:
```bash
pip install pyinstaller PyQt6
pyinstaller --onefile --noconsole --name "converter" converter.py
```
