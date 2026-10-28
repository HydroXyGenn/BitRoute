"""
ui/widgets.py
Global custom PyQt6 widgets for IPv4 Subnet Toolkit v1.2.0:
1. IpLineEdit (Smart Auto-Dot: Space/Comma dot insertion, 3-digit dot, and 2-digit >= 26 auto-dot)
2. MinecraftTipBanner (12-second rotating course & app tip bar at the bottom of MainWindow)
3. AdvancementToast (Minecraft-style achievement banner shown for 3 seconds on clean solves)
"""

from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt, QTimer

from engine.tips_bank import Advancement, TipsAndStreakManager


class IpLineEdit(QLineEdit):
    """
    Smart IPv4 input field with zero-friction dot insertion:
    - Space or Comma inserts '.' or steps over an existing '.'
    - Typing 3 digits in the current octet auto-inserts '.'
    - v1.2.0 Upgrade: Typing 2 digits >= 26 (e.g., 32, 68, 99) auto-inserts '.'
      immediately because no valid 3-digit IPv4 octet (<= 255) can begin with >= 26.
    """

    def keyPressEvent(self, event):
        key = event.key()
        text = self.text()
        pos = self.cursorPosition()

        # Spacebar or Comma effortlessly inserts a dot or steps over existing dot
        if key in (Qt.Key.Key_Space, Qt.Key.Key_Comma):
            if pos > 0 and text[pos - 1] not in ". ":
                if text.count(".") < 3:
                    self.insert(".")
                    return
            elif pos < len(text) and text[pos] == ".":
                self.setCursorPosition(pos + 1)
                return
            return

        super().keyPressEvent(event)

        # Auto-insert dot when 3 digits are typed OR 2 digits with value >= 26
        if event.text().isdigit():
            cur_text = self.text()
            cur_pos = self.cursorPosition()
            if cur_pos == len(cur_text):
                last_dot = cur_text.rfind(".")
                last_space = cur_text.rfind(" ")
                sep = max(last_dot, last_space)
                octet = cur_text[sep + 1:] if sep != -1 else cur_text
                dots_count = cur_text.count(".") + cur_text.count(" ")

                if dots_count < 3 and octet.isdigit():
                    val = int(octet)
                    if len(octet) == 3 or (len(octet) == 2 and val >= 26):
                        self.insert(".")


class MinecraftTipBanner(QFrame):
    """
    Bottom status banner styled like Minecraft splash/tooltip tips.
    Rotates automatically every 12 seconds or on clicking 'Nouvelle Astuce'.
    """

    def __init__(self, manager: TipsAndStreakManager, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.setObjectName("tipBanner")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 6, 14, 6)
        layout.setSpacing(12)

        self.lbl_tip = QLabel(self.manager.current_tip().formatted)
        self.lbl_tip.setObjectName("tipBannerLabel")
        self.lbl_tip.setWordWrap(True)
        self.lbl_tip.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lbl_tip.mousePressEvent = lambda _e: self.advance_tip(randomize=False)

        self.btn_random_tip = QPushButton("Nouvelle Astuce")
        self.btn_random_tip.setObjectName("btnNextTip")
        self.btn_random_tip.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_random_tip.clicked.connect(lambda: self.advance_tip(randomize=True))

        layout.addWidget(self.lbl_tip, stretch=1)
        layout.addWidget(self.btn_random_tip)

        # 12-second rotation timer
        self.timer = QTimer(self)
        self.timer.setInterval(12000)
        self.timer.timeout.connect(lambda: self.advance_tip(randomize=False))
        self.timer.start()

    def advance_tip(self, randomize: bool = False):
        tip = self.manager.next_tip(randomize=randomize)
        self.lbl_tip.setText(tip.formatted)


class AdvancementToast(QFrame):
    """
    Status banner that appears for 3 seconds
    when the user completes an exercise without clicking 'Show'.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("advancementToast")
        self.setVisible(False)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(12)

        self.lbl_title = QLabel("Progrès débloqué !")
        self.lbl_title.setObjectName("advancementTitle")

        self.lbl_desc = QLabel("")
        self.lbl_desc.setObjectName("advancementDesc")

        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_desc, stretch=1)

        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.setInterval(3200)
        self.hide_timer.timeout.connect(lambda: self.setVisible(False))

    def show_advancement(self, adv: Advancement, streak: int):
        self.lbl_title.setText(f"Progrès débloqué : [{adv.title}]")
        self.lbl_desc.setText(f"{adv.description}  (Série : {streak})")
        self.setVisible(True)
        self.hide_timer.start()
