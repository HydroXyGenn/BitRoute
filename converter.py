import sys
import random
import ipaddress
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton,
    QCheckBox, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt


class BinaryConverterTab(QWidget):
    """Tab 1: 8-bit IPv4 Octet Binary Converter with 3-way inputs (Binary, Decimal, Hex)."""
    def __init__(self):
        super().__init__()
        self.bit_values = [128, 64, 32, 16, 8, 4, 2, 1]
        self.checkboxes = []
        self.bit_cards = []
        self._updating = False
        self.current_value = 0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 20, 28, 20)
        layout.setSpacing(16)

        # Header card
        header_card = QFrame()
        header_card.setObjectName("headerCard")
        header_layout = QVBoxLayout(header_card)
        header_layout.setContentsMargins(20, 14, 20, 14)
        header_layout.setSpacing(4)

        title = QLabel("IPv4 Octet 8-Bit Binary Converter")
        title.setObjectName("tabTitle")
        subtitle = QLabel("Toggle bits or type directly into Binary, Decimal, or Hexadecimal inputs to convert values live.")
        subtitle.setObjectName("tabSubtitle")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addWidget(header_card)

        # Main Converter Card
        card = QFrame()
        card.setObjectName("mainCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(22, 20, 22, 20)
        card_layout.setSpacing(20)

        # 8-bit checkboxes row
        bits_layout = QHBoxLayout()
        bits_layout.setSpacing(10)

        for i, val in enumerate(self.bit_values):
            bit_box = QFrame()
            bit_box.setObjectName("bitBox")
            bit_box_layout = QVBoxLayout(bit_box)
            bit_box_layout.setContentsMargins(8, 10, 8, 10)
            bit_box_layout.setSpacing(6)
            bit_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            val_label = QLabel(str(val))
            val_label.setObjectName("bitWeightLabel")
            val_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            cb = QCheckBox()
            cb.setObjectName("bitCheckBox")
            cb.setCursor(Qt.CursorShape.PointingHandCursor)
            cb.stateChanged.connect(self.on_checkbox_toggled)
            self.checkboxes.append(cb)

            bit_pos = QLabel(f"Bit {7 - i}")
            bit_pos.setObjectName("bitPosLabel")
            bit_pos.setAlignment(Qt.AlignmentFlag.AlignCenter)

            bit_box_layout.addWidget(val_label)
            bit_box_layout.addWidget(cb)
            bit_box_layout.addWidget(bit_pos)

            self.bit_cards.append(bit_box)
            bits_layout.addWidget(bit_box)

        card_layout.addLayout(bits_layout)

        # Multi-Format Interactive Input & Display Boxes
        inputs_layout = QHBoxLayout()
        inputs_layout.setSpacing(16)

        # 1. Binary Input Card
        bin_card = QFrame()
        bin_card.setObjectName("resultBox")
        bin_layout = QVBoxLayout(bin_card)
        bin_layout.setContentsMargins(14, 10, 14, 10)
        bin_title = QLabel("Binary (8-bit)")
        bin_title.setObjectName("resultTitle")
        self.bin_input = QLineEdit("00000000")
        self.bin_input.setObjectName("syncInput")
        self.bin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bin_input.setPlaceholderText("00000000")
        self.bin_input.textEdited.connect(self.on_binary_edited)
        bin_layout.addWidget(bin_title)
        bin_layout.addWidget(self.bin_input)
        inputs_layout.addWidget(bin_card)

        # 2. Decimal Input Card
        dec_card = QFrame()
        dec_card.setObjectName("resultBox")
        dec_layout = QVBoxLayout(dec_card)
        dec_layout.setContentsMargins(14, 10, 14, 10)
        dec_title = QLabel("Decimal (0 - 255)")
        dec_title.setObjectName("resultTitle")
        self.dec_input = QLineEdit("0")
        self.dec_input.setObjectName("syncInput")
        self.dec_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dec_input.setPlaceholderText("0")
        self.dec_input.textEdited.connect(self.on_decimal_edited)
        dec_layout.addWidget(dec_title)
        dec_layout.addWidget(self.dec_input)
        inputs_layout.addWidget(dec_card)

        # 3. Hexadecimal Input Card
        hex_card = QFrame()
        hex_card.setObjectName("resultBox")
        hex_layout = QVBoxLayout(hex_card)
        hex_layout.setContentsMargins(14, 10, 14, 10)
        hex_title = QLabel("Hexadecimal (00 - FF)")
        hex_title.setObjectName("resultTitle")
        self.hex_input = QLineEdit("0x00")
        self.hex_input.setObjectName("syncInput")
        self.hex_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hex_input.setPlaceholderText("0x00")
        self.hex_input.textEdited.connect(self.on_hex_edited)
        hex_layout.addWidget(hex_title)
        hex_layout.addWidget(self.hex_input)
        inputs_layout.addWidget(hex_card)

        card_layout.addLayout(inputs_layout)

        # Quick Control Buttons
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        quick_label = QLabel("Quick Presets:")
        quick_label.setObjectName("inputLabel")

        btn_all_on = QPushButton("All 1s (255)")
        btn_all_on.setObjectName("toolBtn")
        btn_all_on.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_all_on.clicked.connect(self.set_all_ones)

        btn_clear = QPushButton("Clear All (0)")
        btn_clear.setObjectName("toolBtn")
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.clicked.connect(self.clear_all)

        btn_invert = QPushButton("Invert Bits")
        btn_invert.setObjectName("toolBtn")
        btn_invert.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_invert.clicked.connect(self.invert_bits)

        controls_layout.addWidget(quick_label)
        controls_layout.addWidget(btn_all_on)
        controls_layout.addWidget(btn_clear)
        controls_layout.addWidget(btn_invert)
        controls_layout.addStretch()

        card_layout.addLayout(controls_layout)
        layout.addWidget(card)
        layout.addStretch()

        self.apply_value(0, source="init")

    def apply_value(self, val: int, source: str = ""):
        """Central update method ensuring all widgets synchronize seamlessly."""
        val = max(0, min(255, val))
        self.current_value = val

        self._updating = True
        try:
            # 1. Update Checkboxes and Bit Card Styles
            for i, bit_val in enumerate(self.bit_values):
                is_on = bool(val & bit_val)
                if self.checkboxes[i].isChecked() != is_on:
                    self.checkboxes[i].setChecked(is_on)
                self.bit_cards[i].setProperty("active", is_on)
                self.bit_cards[i].style().unpolish(self.bit_cards[i])
                self.bit_cards[i].style().polish(self.bit_cards[i])

            # 2. Update Binary Input Field
            if source != "binary":
                bin_str = f"{val:08b}"
                self.bin_input.setText(bin_str)

            # 3. Update Decimal Input Field
            if source != "decimal":
                self.dec_input.setText(str(val))

            # 4. Update Hex Input Field
            if source != "hex":
                self.hex_input.setText(f"0x{val:02X}")
        finally:
            self._updating = False

    def on_checkbox_toggled(self):
        if self._updating:
            return
        total = 0
        for i, cb in enumerate(self.checkboxes):
            if cb.isChecked():
                total += self.bit_values[i]
        self.apply_value(total, source="checkbox")

    def on_binary_edited(self, text):
        if self._updating:
            return
        cleaned = text.replace(" ", "").replace("_", "")
        # Filter only 0 and 1
        filtered = "".join([c for c in cleaned if c in "01"])[:8]
        if filtered:
            val = int(filtered, 2)
        else:
            val = 0
        self.apply_value(val, source="binary")

    def on_decimal_edited(self, text):
        if self._updating:
            return
        text = text.strip()
        if not text:
            val = 0
        elif text.isdigit():
            val = min(255, int(text))
        else:
            return
        self.apply_value(val, source="decimal")

    def on_hex_edited(self, text):
        if self._updating:
            return
        cleaned = text.strip().lower()
        if cleaned.startswith("0x"):
            cleaned = cleaned[2:]
        # Take up to 2 hex digits
        cleaned = "".join([c for c in cleaned if c in "0123456789abcdef"])[:2]
        if cleaned:
            val = int(cleaned, 16)
        else:
            val = 0
        self.apply_value(val, source="hex")

    def set_all_ones(self):
        self.apply_value(255, source="preset")

    def clear_all(self):
        self.apply_value(0, source="preset")

    def invert_bits(self):
        new_val = (~self.current_value) & 0xFF
        self.apply_value(new_val, source="preset")


class IpLineEdit(QLineEdit):
    """Smart IPv4 input field that enables effortless typing without manual dot keys."""
    def keyPressEvent(self, event):
        key = event.key()
        text = self.text()
        pos = self.cursorPosition()

        # Spacebar or Comma effortlessly inserts a dot or steps over existing dot
        if key in (Qt.Key.Key_Space, Qt.Key.Key_Comma):
            if pos > 0 and text[pos - 1] not in ". ":
                if text.count('.') < 3:
                    self.insert(".")
                    return
            elif pos < len(text) and text[pos] == '.':
                self.setCursorPosition(pos + 1)
                return
            return

        super().keyPressEvent(event)

        # Auto-insert dot when 3 digits are typed in the current octet
        if event.text().isdigit():
            cur_text = self.text()
            cur_pos = self.cursorPosition()
            if cur_pos == len(cur_text):
                last_dot = cur_text.rfind('.')
                last_space = cur_text.rfind(' ')
                sep = max(last_dot, last_space)
                octet = cur_text[sep + 1:] if sep != -1 else cur_text
                dots_count = cur_text.count('.') + cur_text.count(' ')
                if len(octet) == 3 and dots_count < 3:
                    self.insert(".")


class SubnetPracticeTab(QWidget):
    """Tab 2: Subnet Practice precisely mirroring the reference image."""
    def __init__(self):
        super().__init__()
        self.current_ip = "104.172.78.239"
        self.current_cidr = 23
        self.answers = {}
        self.input_fields = {}
        self.status_labels = {}
        self.answer_fields = {}
        self.show_buttons = {}
        self.answer_visible = {}
        self.init_ui()
        self.generate_new_problem()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 22, 32, 22)
        main_layout.setSpacing(16)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ----------------- Top Header Bar -----------------
        # Matches reference image:
        # [ Target IP address   [ 104 . 172 . 78 . 239 ]  /  [ 23 ]   [ Next Problem ] ]
        top_bar_container = QFrame()
        top_bar_container.setObjectName("topBarContainer")
        top_bar_layout = QHBoxLayout(top_bar_container)
        top_bar_layout.setContentsMargins(20, 10, 20, 10)
        top_bar_layout.setSpacing(12)
        top_bar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        target_label = QLabel("Target IP address")
        target_label.setObjectName("targetLabel")

        # IP display pill box
        self.ip_display = QLabel("104 . 172 . 78 . 239")
        self.ip_display.setObjectName("targetIpDisplay")
        self.ip_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        slash_label = QLabel("/")
        slash_label.setObjectName("slashLabel")

        # CIDR display pill box
        self.cidr_display = QLabel("23")
        self.cidr_display.setObjectName("targetCidrDisplay")
        self.cidr_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Next Problem button
        self.btn_next = QPushButton("Next Problem")
        self.btn_next.setObjectName("btnNextProblem")
        self.btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_next.clicked.connect(self.generate_new_problem)

        top_bar_layout.addWidget(target_label)
        top_bar_layout.addWidget(self.ip_display)
        top_bar_layout.addWidget(slash_label)
        top_bar_layout.addWidget(self.cidr_display)
        top_bar_layout.addSpacing(10)
        top_bar_layout.addWidget(self.btn_next)

        main_layout.addWidget(top_bar_container, alignment=Qt.AlignmentFlag.AlignCenter)

        # ----------------- Main Table Card -----------------
        table_card = QFrame()
        table_card.setObjectName("tableCard")
        grid = QGridLayout(table_card)
        grid.setContentsMargins(28, 20, 28, 24)
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(15)

        # Headers: [ empty / RowName ] | [ IP address ] | [ Correct? ] | [ Answer ] | [ Show ]
        h_ip = QLabel("IP address")
        h_ip.setObjectName("columnHeader")
        h_ip.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h_correct = QLabel("Correct?")
        h_correct.setObjectName("columnHeader")
        h_correct.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h_answer = QLabel("Answer")
        h_answer.setObjectName("columnHeader")
        h_answer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h_show = QLabel("Show")
        h_show.setObjectName("columnHeader")
        h_show.setAlignment(Qt.AlignmentFlag.AlignCenter)

        grid.addWidget(h_ip, 0, 1)
        grid.addWidget(h_correct, 0, 2)
        grid.addWidget(h_answer, 0, 3)
        grid.addWidget(h_show, 0, 4)

        # Row categories
        self.row_keys = ["Network", "First Host", "Last Host", "Broadcast", "Next Subnet"]

        for row_idx, key in enumerate(self.row_keys, start=1):
            # Row Name label
            lbl_name = QLabel(key)
            lbl_name.setObjectName("rowLabel")
            lbl_name.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

            # User IP address input using smart IpLineEdit
            inp = IpLineEdit()
            inp.setObjectName("subnetInput")
            inp.setPlaceholderText(".     .     .")
            inp.setAlignment(Qt.AlignmentFlag.AlignCenter)
            inp.setMinimumWidth(190)
            inp.setMaximumWidth(220)
            inp.textChanged.connect(lambda text, k=key: self.validate_input(k))
            self.input_fields[key] = inp

            # Status label (Correct?)
            status = QLabel("✕")
            status.setObjectName("statusWrong")
            status.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.status_labels[key] = status

            # Answer field (read-only)
            ans = QLineEdit()
            ans.setObjectName("answerField")
            ans.setReadOnly(True)
            ans.setPlaceholderText(".     .     .")
            ans.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ans.setMinimumWidth(190)
            ans.setMaximumWidth(220)
            self.answer_fields[key] = ans
            self.answer_visible[key] = False

            # Show button
            btn_show = QPushButton("Show")
            btn_show.setObjectName("btnShow")
            btn_show.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_show.clicked.connect(lambda _, k=key: self.toggle_show_answer(k))
            self.show_buttons[key] = btn_show

            grid.addWidget(lbl_name, row_idx, 0)
            grid.addWidget(inp, row_idx, 1)
            grid.addWidget(status, row_idx, 2)
            grid.addWidget(ans, row_idx, 3)
            grid.addWidget(btn_show, row_idx, 4)

        main_layout.addWidget(table_card)

    def generate_new_problem(self):
        """Generates random IPv4 and CIDR prefix (between /8 and /30) and calculates answers."""
        first_oct = random.choice([
            random.randint(1, 126),
            random.randint(128, 223)
        ])
        o2 = random.randint(0, 255)
        o3 = random.randint(0, 255)
        o4 = random.randint(1, 254)
        cidr = random.randint(8, 30)

        ip_str = f"{first_oct}.{o2}.{o3}.{o4}"
        self.current_ip = ip_str
        self.current_cidr = cidr

        # Calculate using ipaddress module
        net = ipaddress.IPv4Network(f"{ip_str}/{cidr}", strict=False)

        net_addr = net.network_address
        bcast_addr = net.broadcast_address
        first_host = net_addr + 1
        last_host = bcast_addr - 1
        next_sub_int = (int(net_addr) + net.num_addresses) % (2**32)
        next_subnet = ipaddress.IPv4Address(next_sub_int)

        self.answers = {
            "Network": str(net_addr),
            "First Host": str(first_host),
            "Last Host": str(last_host),
            "Broadcast": str(bcast_addr),
            "Next Subnet": str(next_subnet)
        }

        # Update Top Bar display with spaced dots like the reference photo
        octets = ip_str.split('.')
        self.ip_display.setText(f"{octets[0]}  .  {octets[1]}  .  {octets[2]}  .  {octets[3]}")
        self.cidr_display.setText(str(cidr))

        # Reset all fields
        for key in self.row_keys:
            self.input_fields[key].blockSignals(True)
            self.input_fields[key].clear()
            self.input_fields[key].blockSignals(False)

            self.status_labels[key].setText("✕")
            self.status_labels[key].setObjectName("statusWrong")
            self.status_labels[key].style().unpolish(self.status_labels[key])
            self.status_labels[key].style().polish(self.status_labels[key])

            self.answer_visible[key] = False
            self.answer_fields[key].setText("")
            self.show_buttons[key].setText("Show")

    def validate_input(self, key):
        """Real-time validation supporting spaces, dots, commas, or direct numbers."""
        user_val = self.input_fields[key].text().strip()
        cleaned_parts = []
        cur_oct = ""
        for ch in user_val:
            if ch.isdigit():
                cur_oct += ch
            else:
                if cur_oct:
                    cleaned_parts.append(cur_oct)
                    cur_oct = ""
        if cur_oct:
            cleaned_parts.append(cur_oct)

        normalized_user = ".".join(cleaned_parts)
        correct_val = self.answers.get(key, "")

        if normalized_user == correct_val:
            self.status_labels[key].setText("✓")
            self.status_labels[key].setObjectName("statusCorrect")
        else:
            self.status_labels[key].setText("✕")
            self.status_labels[key].setObjectName("statusWrong")

        self.status_labels[key].style().unpolish(self.status_labels[key])
        self.status_labels[key].style().polish(self.status_labels[key])

    def toggle_show_answer(self, key):
        """Toggles answer visibility in the read-only field."""
        self.answer_visible[key] = not self.answer_visible[key]
        if self.answer_visible[key]:
            self.answer_fields[key].setText(self.answers.get(key, ""))
            self.show_buttons[key].setText("Hide")
        else:
            self.answer_fields[key].setText("")
            self.show_buttons[key].setText("Show")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IPv4 Binary & Subnet Practice")
        self.resize(880, 580)
        self.setMinimumSize(800, 520)
        self.is_dark_mode = False

        # Central Tabs container
        self.tabs = QTabWidget()
        self.tabs.setObjectName("mainTabs")

        self.tab_binary = BinaryConverterTab()
        self.tab_subnet = SubnetPracticeTab()

        self.tabs.addTab(self.tab_binary, "Binary Converter")
        self.tabs.addTab(self.tab_subnet, "Subnet Practice")

        # Dark Mode Toggle Button in the top right corner of the tab bar
        self.btn_dark_toggle = QPushButton("💻 Hacker Dark")
        self.btn_dark_toggle.setObjectName("btnThemeToggle")
        self.btn_dark_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_dark_toggle.clicked.connect(self.toggle_dark_mode)
        self.tabs.setCornerWidget(self.btn_dark_toggle, Qt.Corner.TopRightCorner)

        self.setCentralWidget(self.tabs)
        self.apply_theme()

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.btn_dark_toggle.setText("☀️ Light Mode")
        else:
            self.btn_dark_toggle.setText("💻 Hacker Dark")
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet(self.get_dark_qss())
        else:
            self.setStyleSheet(self.get_light_qss())

    def get_light_qss(self) -> str:
        return """
        QMainWindow {
            background-color: #F4F7FB;
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
        }

        QWidget {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            color: #1E293B;
            font-size: 14px;
        }

        QTabWidget::pane {
            border: 1px solid #E2E8F0;
            background: #F8FAFC;
            border-top: none;
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
        }

        QTabBar::tab {
            background: #E2E8F0;
            color: #475569;
            font-weight: 600;
            font-size: 14px;
            padding: 10px 24px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            margin-right: 4px;
            border: 1px solid #CBD5E1;
            border-bottom: none;
        }

        QTabBar::tab:selected {
            background: #F8FAFC;
            color: #1E40AF;
            border-top: 3px solid #2563EB;
            border-bottom: 1px solid #F8FAFC;
        }

        QTabBar::tab:hover:!selected {
            background: #EDF2F7;
            color: #1E293B;
        }

        #btnThemeToggle {
            background-color: #FFFFFF;
            border: 1.5px solid #CBD5E1;
            border-radius: 8px;
            padding: 6px 14px;
            margin-right: 8px;
            margin-bottom: 4px;
            font-weight: 600;
            color: #334155;
            font-size: 13px;
        }

        #btnThemeToggle:hover {
            background-color: #F1F5F9;
            color: #0F172A;
        }

        #headerCard, #mainCard, #tableCard {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
        }

        #tabTitle {
            font-size: 17px;
            font-weight: 700;
            color: #0F172A;
        }

        #tabSubtitle {
            font-size: 13px;
            color: #64748B;
        }

        #bitBox {
            background-color: #F8FAFC;
            border: 1.5px solid #CBD5E1;
            border-radius: 10px;
        }

        #bitBox[active="true"] {
            background-color: #EFF6FF;
            border: 2px solid #3B82F6;
        }

        #bitWeightLabel {
            font-size: 16px;
            font-weight: 700;
            color: #1E293B;
        }

        #bitPosLabel {
            font-size: 12px;
            color: #64748B;
            font-weight: 500;
        }

        QCheckBox#bitCheckBox::indicator {
            width: 22px;
            height: 22px;
            border-radius: 6px;
            border: 2px solid #94A3B8;
            background-color: #FFFFFF;
        }

        QCheckBox#bitCheckBox::indicator:checked {
            border: 2px solid #2563EB;
            background-color: #2563EB;
        }

        #resultBox {
            background-color: #F8FAFC;
            border: 1.5px solid #CBD5E1;
            border-radius: 10px;
        }

        #resultTitle {
            font-size: 12px;
            font-weight: 700;
            color: #475569;
            text-transform: uppercase;
        }

        #syncInput {
            border: 1.5px solid #94A3B8;
            border-radius: 8px;
            padding: 6px 10px;
            font-size: 16px;
            font-weight: 700;
            color: #0F172A;
            background: #FFFFFF;
            font-family: 'Consolas', 'Courier New', monospace;
        }

        #syncInput:focus {
            border: 2px solid #2563EB;
        }

        #inputLabel {
            font-weight: 600;
            color: #334155;
            font-size: 13px;
        }

        #toolBtn {
            background-color: #F1F5F9;
            border: 1px solid #CBD5E1;
            border-radius: 8px;
            color: #334155;
            font-weight: 600;
            padding: 6px 14px;
            font-size: 13px;
        }

        #toolBtn:hover {
            background-color: #E2E8F0;
            color: #0F172A;
        }

        #topBarContainer {
            background-color: #FFFFFF;
            border: 1.5px solid #DCE6F1;
            border-radius: 14px;
        }

        #targetLabel {
            font-size: 15px;
            font-weight: 700;
            color: #0F172A;
            margin-right: 6px;
        }

        #targetIpDisplay {
            border: 1.5px solid #64748B;
            border-radius: 10px;
            padding: 5px 16px;
            font-size: 15px;
            font-weight: 700;
            color: #0F172A;
            background-color: #FFFFFF;
            letter-spacing: 1px;
        }

        #slashLabel {
            font-size: 18px;
            font-weight: 700;
            color: #475569;
        }

        #targetCidrDisplay {
            border: 1.5px solid #64748B;
            border-radius: 8px;
            padding: 5px 14px;
            font-size: 15px;
            font-weight: 700;
            color: #0F172A;
            background-color: #FFFFFF;
        }

        #btnNextProblem {
            background-color: #1D4ED8;
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 7px 20px;
            font-size: 14px;
            font-weight: 700;
        }

        #btnNextProblem:hover {
            background-color: #2563EB;
        }

        #btnNextProblem:pressed {
            background-color: #1E40AF;
        }

        #columnHeader {
            font-size: 14px;
            font-weight: 700;
            color: #1E293B;
            padding-bottom: 4px;
        }

        #rowLabel {
            font-size: 15px;
            font-weight: 700;
            color: #1E293B;
            padding-right: 8px;
        }

        #subnetInput {
            border: 1.5px solid #64748B;
            border-radius: 10px;
            padding: 6px 12px;
            font-size: 15px;
            font-weight: 500;
            color: #0F172A;
            background-color: #FFFFFF;
        }

        #subnetInput:focus {
            border: 2px solid #2563EB;
        }

        #answerField {
            border: 1.5px solid #94A3B8;
            border-radius: 10px;
            padding: 6px 12px;
            font-size: 15px;
            font-weight: 500;
            color: #334155;
            background-color: #F8FAFC;
        }

        #statusWrong {
            font-size: 18px;
            font-weight: 900;
            color: #991B1B;
        }

        #statusCorrect {
            font-size: 18px;
            font-weight: 900;
            color: #15803D;
        }

        #btnShow {
            background-color: transparent;
            color: #0284C7;
            border: 1px solid #BAE6FD;
            border-radius: 8px;
            padding: 5px 14px;
            font-size: 13px;
            font-weight: 600;
        }

        #btnShow:hover {
            background-color: #E0F2FE;
            color: #0369A1;
        }
        """

    def get_dark_qss(self) -> str:
        return """
        /* ================= HACKER CONSOLE BLACK & GREEN THEME ================= */
        QMainWindow {
            background-color: #000000;
            font-family: 'Consolas', 'Courier New', 'Lucida Console', monospace;
        }

        QWidget {
            font-family: 'Consolas', 'Courier New', 'Lucida Console', monospace;
            color: #00FF66;
            font-size: 14px;
        }

        QTabWidget::pane {
            border: 1.5px solid #00551A;
            background: #020702;
            border-top: none;
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
        }

        QTabBar::tab {
            background: #061106;
            color: #00AA44;
            font-weight: 700;
            font-size: 14px;
            padding: 10px 24px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            margin-right: 4px;
            border: 1.5px solid #004414;
            border-bottom: none;
        }

        QTabBar::tab:selected {
            background: #020702;
            color: #00FF66;
            border-top: 3px solid #00FF66;
            border-bottom: 1.5px solid #020702;
        }

        QTabBar::tab:hover:!selected {
            background: #0D1F0D;
            color: #33FF88;
        }

        #btnThemeToggle {
            background-color: #061106;
            border: 1.5px solid #00AA44;
            border-radius: 8px;
            padding: 6px 14px;
            margin-right: 8px;
            margin-bottom: 4px;
            font-weight: 700;
            color: #00FF66;
            font-size: 13px;
        }

        #btnThemeToggle:hover {
            background-color: #00FF66;
            color: #000000;
        }

        #headerCard, #mainCard, #tableCard {
            background-color: #040A04;
            border: 1.5px solid #00551A;
            border-radius: 12px;
        }

        #tabTitle {
            font-size: 17px;
            font-weight: 700;
            color: #00FF66;
            letter-spacing: 1px;
        }

        #tabSubtitle {
            font-size: 13px;
            color: #00CC55;
        }

        #bitBox {
            background-color: #010401;
            border: 1.5px solid #004414;
            border-radius: 10px;
        }

        #bitBox[active="true"] {
            background-color: #00220A;
            border: 2px solid #00FF66;
        }

        #bitWeightLabel {
            font-size: 16px;
            font-weight: 700;
            color: #00FF66;
        }

        #bitPosLabel {
            font-size: 12px;
            color: #009933;
            font-weight: 600;
        }

        QCheckBox#bitCheckBox::indicator {
            width: 22px;
            height: 22px;
            border-radius: 6px;
            border: 2px solid #007722;
            background-color: #000000;
        }

        QCheckBox#bitCheckBox::indicator:checked {
            border: 2px solid #00FF66;
            background-color: #00FF66;
        }

        #resultBox {
            background-color: #010401;
            border: 1.5px solid #00551A;
            border-radius: 10px;
        }

        #resultTitle {
            font-size: 12px;
            font-weight: 700;
            color: #00CC55;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        #syncInput {
            border: 1.5px solid #007722;
            border-radius: 8px;
            padding: 6px 10px;
            font-size: 16px;
            font-weight: 700;
            color: #00FF66;
            background: #030803;
            font-family: 'Consolas', 'Courier New', monospace;
        }

        #syncInput:focus {
            border: 2px solid #00FF66;
            background: #001405;
        }

        #inputLabel {
            font-weight: 700;
            color: #00CC55;
            font-size: 13px;
        }

        #toolBtn {
            background-color: #040A04;
            border: 1.5px solid #007722;
            border-radius: 8px;
            color: #00FF66;
            font-weight: 700;
            padding: 6px 14px;
            font-size: 13px;
        }

        #toolBtn:hover {
            background-color: #00FF66;
            color: #000000;
        }

        #topBarContainer {
            background-color: #040A04;
            border: 1.5px solid #00551A;
            border-radius: 14px;
        }

        #targetLabel {
            font-size: 15px;
            font-weight: 700;
            color: #00FF66;
            margin-right: 6px;
            letter-spacing: 0.5px;
        }

        #targetIpDisplay {
            border: 1.5px solid #00882E;
            border-radius: 10px;
            padding: 5px 16px;
            font-size: 15px;
            font-weight: 700;
            color: #00FF66;
            background-color: #000000;
            letter-spacing: 1px;
        }

        #slashLabel {
            font-size: 18px;
            font-weight: 700;
            color: #00AA44;
        }

        #targetCidrDisplay {
            border: 1.5px solid #00882E;
            border-radius: 8px;
            padding: 5px 14px;
            font-size: 15px;
            font-weight: 700;
            color: #00FF66;
            background-color: #000000;
        }

        #btnNextProblem {
            background-color: #00551A;
            color: #00FF66;
            border: 1.5px solid #00FF66;
            border-radius: 8px;
            padding: 7px 20px;
            font-size: 14px;
            font-weight: 700;
        }

        #btnNextProblem:hover {
            background-color: #00FF66;
            color: #000000;
        }

        #btnNextProblem:pressed {
            background-color: #003310;
            color: #00FF66;
        }

        #columnHeader {
            font-size: 14px;
            font-weight: 700;
            color: #00CC55;
            padding-bottom: 4px;
        }

        #rowLabel {
            font-size: 15px;
            font-weight: 700;
            color: #00FF66;
            padding-right: 8px;
        }

        #subnetInput {
            border: 1.5px solid #007722;
            border-radius: 10px;
            padding: 6px 12px;
            font-size: 15px;
            font-weight: 600;
            color: #00FF66;
            background-color: #000000;
            font-family: 'Consolas', 'Courier New', monospace;
        }

        #subnetInput:focus {
            border: 2px solid #00FF66;
            background-color: #001405;
        }

        #answerField {
            border: 1.5px solid #004414;
            border-radius: 10px;
            padding: 6px 12px;
            font-size: 15px;
            font-weight: 600;
            color: #00AA44;
            background-color: #020702;
            font-family: 'Consolas', 'Courier New', monospace;
        }

        #statusWrong {
            font-size: 18px;
            font-weight: 900;
            color: #FF3344;
        }

        #statusCorrect {
            font-size: 18px;
            font-weight: 900;
            color: #00FF66;
        }

        #btnShow {
            background-color: #020702;
            color: #00FF66;
            border: 1.5px solid #007722;
            border-radius: 8px;
            padding: 5px 14px;
            font-size: 13px;
            font-weight: 700;
        }

        #btnShow:hover {
            background-color: #00FF66;
            color: #000000;
        }
        """


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
