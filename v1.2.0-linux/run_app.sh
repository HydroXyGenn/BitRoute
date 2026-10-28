#!/usr/bin/env bash
# ==============================================================================
# IPv4 Subnet Toolkit v1.2.0 — Linux Launcher
# Launches the standalone binary ./converter if built, or falls back to Python3.
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -x "$SCRIPT_DIR/converter" ] && [ ! -d "$SCRIPT_DIR/converter" ]; then
    nohup "$SCRIPT_DIR/converter" >/dev/null 2>&1 &
elif [ -x "$SCRIPT_DIR/dist/converter" ]; then
    nohup "$SCRIPT_DIR/dist/converter" >/dev/null 2>&1 &
else
    nohup python3 "$SCRIPT_DIR/converter.py" >/dev/null 2>&1 &
fi
