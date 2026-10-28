"""
ui/main_window.py
MainWindow for IPv4 Subnet Toolkit v1.2.0:
- 4 Tabs (8-Bit Binary + Mask Inspector, Subnet Practice + 32-Bit Drawer, VLSM Express, Flash Drills)
- Top-Right Corner Bar: Streak Counter Badge + Hacker Dark / Light Mode Toggle
- AdvancementToast notification banner on clean solves
- MinecraftTipBanner rotating course & shortcut tips at the bottom
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton
)
from PyQt6.QtCore import Qt

from engine.tips_bank import TipsAndStreakManager
from ui.themes import get_dark_qss, get_light_qss
from ui.widgets import AdvancementToast, MinecraftTipBanner
from ui.tab_binary import BinaryConverterTab
from ui.tab_subnet import SubnetPracticeTab
from ui.tab_vlsm import VlsmLabTab
from ui.tab_drills import FlashDrillsTab


class MainWindow(QMainWindow):
    """Main application window assembling all 4 networking tabs and gamification bars."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BitRoute v1.2.0 — IPv4 Subnet, VLSM & Routing Toolkit (INPT ASEDS)")
        self.resize(1100, 720)
        self.setMinimumSize(980, 620)
        self.is_dark_mode = False

        self.tips_manager = TipsAndStreakManager()

        # Root container
        root_widget = QWidget()
        root_layout = QVBoxLayout(root_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Advancement Toast Banner (hidden by default, shown on clean solve)
        toast_wrapper = QHBoxLayout()
        toast_wrapper.setContentsMargins(16, 6, 16, 0)
        self.advancement_toast = AdvancementToast()
        toast_wrapper.addWidget(self.advancement_toast)
        root_layout.addLayout(toast_wrapper)

        # Central Tabs container
        self.tabs = QTabWidget()
        self.tabs.setObjectName("mainTabs")

        self.tab_binary = BinaryConverterTab()
        self.tab_subnet = SubnetPracticeTab(on_clean_solve=self.handle_clean_solve)
        self.tab_vlsm = VlsmLabTab(on_clean_solve=self.handle_clean_solve)
        self.tab_drills = FlashDrillsTab(on_clean_solve=self.handle_clean_solve)

        self.tabs.addTab(self.tab_binary, "1. Convertisseur 8-Bit")
        self.tabs.addTab(self.tab_subnet, "2. Pratique Sous-Réseau")
        self.tabs.addTab(self.tab_vlsm, "3. Atelier VLSM Express")
        self.tabs.addTab(self.tab_drills, "4. Flash Drills (MTU, LPM, Hex)")

        # Top-Right Corner Widget: Streak Badge + Theme Toggle
        corner_widget = QWidget()
        corner_layout = QHBoxLayout(corner_widget)
        corner_layout.setContentsMargins(4, 2, 8, 4)
        corner_layout.setSpacing(8)

        self.lbl_streak = QLabel("Série : 0")
        self.lbl_streak.setObjectName("streakBadge")

        self.btn_dark_toggle = QPushButton("Hacker Dark")
        self.btn_dark_toggle.setObjectName("btnThemeToggle")
        self.btn_dark_toggle.setFixedWidth(115)
        self.btn_dark_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_dark_toggle.clicked.connect(self.toggle_dark_mode)

        corner_layout.addWidget(self.lbl_streak)
        corner_layout.addWidget(self.btn_dark_toggle)
        self.tabs.setCornerWidget(corner_widget, Qt.Corner.TopRightCorner)

        root_layout.addWidget(self.tabs, stretch=1)

        # Bottom Minecraft Tip Banner
        self.tip_banner = MinecraftTipBanner(self.tips_manager)
        root_layout.addWidget(self.tip_banner)

        self.setCentralWidget(root_widget)
        self.apply_theme()

    def handle_clean_solve(self, category_key: str):
        """Called when any exercise is solved without clicking 'Show'."""
        adv = self.tips_manager.record_clean_solve(category_key)
        self.lbl_streak.setText(f"Série : {self.tips_manager.streak}")
        if adv is not None:
            self.advancement_toast.show_advancement(adv, self.tips_manager.streak)

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.btn_dark_toggle.setText("Light Mode")
        else:
            self.btn_dark_toggle.setText("Hacker Dark")
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet(get_dark_qss())
        else:
            self.setStyleSheet(get_light_qss())
