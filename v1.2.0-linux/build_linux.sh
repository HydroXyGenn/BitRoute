#!/usr/bin/env bash
# ==============================================================================
# IPv4 Subnet Toolkit v1.2.0 — Standalone Linux Binary Builder (RHEL 10 / Fedora)
# Produces a single-file Linux ELF executable: ./converter (and ./dist/converter)
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=================================================================="
echo " 🌐 IPv4 Subnet Toolkit v1.2.0 — Linux Standalone Binary Builder"
echo "=================================================================="

# 1. Check / Install RHEL 10 / Fedora / CentOS (dnf) system dependencies
if command -v dnf >/dev/null 2>&1; then
    echo "[1/5] Détection de RHEL / Fedora / CentOS (dnf)..."
    MISSING_PKGS=()
    for pkg in python3 python3-pip binutils xcb-util-cursor xcb-util-wm xcb-util-image xcb-util-keysyms xcb-util-renderutil libxkbcommon-x11; do
        if ! rpm -q "$pkg" >/dev/null 2>&1; then
            MISSING_PKGS+=("$pkg")
        fi
    done

    if [ ${#MISSING_PKGS[@]} -gt 0 ]; then
        echo "      Tentative d'installation des paquets système (${MISSING_PKGS[*]})..."
        sudo dnf install -y "${MISSING_PKGS[@]}" || echo "      [Info] Certains paquets optionnels n'ont pas pu être installés via dnf (ex: abonnement RHEL inactif). Poursuite avec Wayland/Qt6 intégré..."
    else
        echo "      Tous les paquets système requis sont déjà installés."
    fi
elif command -v apt-get >/dev/null 2>&1; then
    echo "[1/5] Détection de Debian / Ubuntu / Kali (apt)..."
    sudo apt-get update && sudo apt-get install -y python3 python3-venv python3-pip binutils libxcb-cursor0 libxkbcommon-x11-0 || true
elif command -v pacman >/dev/null 2>&1; then
    echo "[1/5] Détection de Arch / Manjaro (pacman)..."
    sudo pacman -S --needed --noconfirm python python-pip binutils xcb-util-cursor libxkbcommon-x11 || true
fi

# 2. Create isolated build virtualenv in /tmp (works even on VMware Shared Folders /mnt/hgfs)
BUILD_VENV="/tmp/ipv4_toolkit_build_venv"
BUILD_WORK="/tmp/ipv4_toolkit_build_work"

echo "[2/5] Préparation de l'environnement de build isolé ($BUILD_VENV)..."
rm -rf "$BUILD_VENV" "$BUILD_WORK"
if python3 -m venv "$BUILD_VENV" 2>/dev/null; then
    source "$BUILD_VENV/bin/activate"
    PIP_CMD="pip"
    PYINSTALLER_CMD="pyinstaller"
else
    echo "      [Info] python3-venv indisponible, utilisation de pip --user..."
    PIP_CMD="python3 -m pip install --user"
    export PATH="$HOME/.local/bin:$PATH"
    PYINSTALLER_CMD="python3 -m PyInstaller"
fi

# 3. Install PyQt6 and PyInstaller
echo "[3/5] Installation de PyQt6 et PyInstaller..."
if [ "$PIP_CMD" = "pip" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
else
    $PIP_CMD -r requirements.txt
fi

# 4. Build standalone single-file Linux binary with PyInstaller
echo "[4/5] Compilation du binaire Linux autonome (PyInstaller)..."
$PYINSTALLER_CMD --clean --noconfirm \
    --workpath "$BUILD_WORK" \
    --distpath "$SCRIPT_DIR/dist" \
    "$SCRIPT_DIR/converter.spec"

if [ "$PIP_CMD" = "pip" ]; then
    deactivate || true
fi
rm -rf "$BUILD_WORK"

# Copy standalone executable to project root (just like converter.exe on Windows)
cp -f "$SCRIPT_DIR/dist/converter" "$SCRIPT_DIR/converter"
chmod +x "$SCRIPT_DIR/converter" "$SCRIPT_DIR/dist/converter" "$SCRIPT_DIR/run_app.sh" "$SCRIPT_DIR/install_desktop_shortcut.sh" 2>/dev/null || true

# 5. Register Desktop & App Menu shortcut
echo "[5/5] Création du raccourci Bureau / Menu Applications RHEL/Fedora..."
if [ -f "$SCRIPT_DIR/install_desktop_shortcut.sh" ]; then
    bash "$SCRIPT_DIR/install_desktop_shortcut.sh"
fi

echo ""
echo "=================================================================="
echo " ✅ Compilation terminée avec succès !"
echo "    • Binaire autonome : $SCRIPT_DIR/converter"
echo "    • Copie dist       : $SCRIPT_DIR/dist/converter"
echo "    • Pour lancer      : ./converter   (ou ./run_app.sh)"
echo "=================================================================="
