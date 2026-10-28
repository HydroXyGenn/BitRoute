#!/usr/bin/env python3
"""BitRoute v1.2.0 (Linux Edition) — Main Entry Point"""

import os
import sys
import ctypes

# On Linux (especially RHEL 10 / Fedora where Wayland is default), prefer native Wayland
# with automatic fallback to XCB so the app runs even if libxcb-cursor0 is absent.
if sys.platform.startswith("linux") and "QT_QPA_PLATFORM" not in os.environ:
    if os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland" or os.environ.get("WAYLAND_DISPLAY"):
        os.environ["QT_QPA_PLATFORM"] = "wayland;xcb"

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow


def get_resource_path(relative_path: str) -> str:
    """Resolve absolute path to resource, working for dev and for PyInstaller _MEIPASS."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def load_application_icon() -> QIcon | None:
    """Load application icon preferring PNG on Linux (native Qt support) with ICO fallback."""
    icon = QIcon()
    loaded = False
    for filename in ("app_icon.png", "app_icon.ico"):
        path = get_resource_path(filename)
        if os.path.exists(path):
            icon.addFile(path)
            loaded = True
    return icon if loaded else None


def main():
    # Set Windows AppUserModelID if running on Windows
    if sys.platform == "win32":
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "inpt.aseds.ipv4subnettoolkit.1.2.0"
            )
        except Exception:
            pass

    app = QApplication(sys.argv)
    app.setApplicationName("BitRoute")
    app.setOrganizationName("INPT-ASEDS")
    # Link window to ipv4-subnet-toolkit.desktop on Linux (GNOME/KDE Wayland & X11 dock icon)
    if hasattr(app, "setDesktopFileName"):
        app.setDesktopFileName("ipv4-subnet-toolkit")

    # Load custom application icon
    app_icon = load_application_icon()
    if app_icon is not None:
        app.setWindowIcon(app_icon)

    window = MainWindow()
    if app_icon is not None:
        window.setWindowIcon(app_icon)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
