#!/usr/bin/env bash
# ==============================================================================
# IPv4 Subnet Toolkit v1.2.0 — Fedora / Linux Desktop Shortcut Installer
# Registers ipv4-subnet-toolkit.desktop in the Application Menu and Desktop.
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ICON_PATH="$SCRIPT_DIR/app_icon.png"

if [ -x "$SCRIPT_DIR/converter" ] && [ ! -d "$SCRIPT_DIR/converter" ]; then
    EXEC_TARGET="\"$SCRIPT_DIR/converter\""
else
    EXEC_TARGET="\"$SCRIPT_DIR/run_app.sh\""
fi

APP_DIR="$HOME/.local/share/applications"
mkdir -p "$APP_DIR"
DESKTOP_FILE="$APP_DIR/ipv4-subnet-toolkit.desktop"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=IPv4 Subnet Toolkit v1.2.0
Comment=INPT ASEDS — Calculateur Binaire, Sous-Réseaux, VLSM, MTU, Routage LPM & Checksum
Exec=$EXEC_TARGET
Path=$SCRIPT_DIR
Icon=$ICON_PATH
Terminal=false
Categories=Education;Network;ComputerScience;Utility;
StartupWMClass=ipv4-subnet-toolkit
EOF

chmod +x "$DESKTOP_FILE"

# Also copy to ~/Desktop or ~/Bureau if present
for ddir in "$HOME/Desktop" "$HOME/Bureau"; do
    if [ -d "$ddir" ]; then
        cp -f "$DESKTOP_FILE" "$ddir/ipv4-subnet-toolkit.desktop"
        chmod +x "$ddir/ipv4-subnet-toolkit.desktop"
        # Mark as trusted on GNOME (Fedora default desktop)
        if command -v gio >/dev/null 2>&1; then
            gio set "$ddir/ipv4-subnet-toolkit.desktop" metadata::trusted true 2>/dev/null || true
        fi
    fi
done

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APP_DIR" 2>/dev/null || true
fi

echo "Raccourci installé : $DESKTOP_FILE"
