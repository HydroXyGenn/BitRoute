"""BitRoute v1.2.0 (IPv4 Subnet, VLSM & Routing Toolkit) — Main Entry Point"""

import os
import sys
import ctypes
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow


def get_resource_path(relative_path: str) -> str:
    """Resolve absolute path to resource, working for dev and for PyInstaller _MEIPASS."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def main():
    # Set Windows AppUserModelID so taskbar groups and shows custom app icon properly
    if sys.platform == "win32":
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "inpt.aseds.ipv4subnettoolkit.1.2.0"
            )
        except Exception:
            pass

    app = QApplication(sys.argv)

    # Load custom application icon
    icon_path = get_resource_path("app_icon.ico")
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
    else:
        app_icon = None

    window = MainWindow()
    if app_icon is not None:
        window.setWindowIcon(app_icon)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

