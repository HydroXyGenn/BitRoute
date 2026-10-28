"""
ui/tab_binary.py
Tab 1: 8-Bit IPv4 Octet Binary Converter + Live Mask & Complement Inspector.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QFrame
)
from PyQt6.QtCore import Qt

from engine.ipv4_math import IPv4MathEngine


class BinaryConverterTab(QWidget):
    """Tab 1: 8-bit IPv4 Octet Binary Converter with 3-way live sync and Mask Inspector."""

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
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(14)

        # Header card
        header_card = QFrame()
        header_card.setObjectName("headerCard")
        header_layout = QVBoxLayout(header_card)
        header_layout.setContentsMargins(18, 12, 18, 12)
        header_layout.setSpacing(3)

        title = QLabel("Convertisseur Binaire 8-Bit & Inspecteur de Masque")
        title.setObjectName("tabTitle")
        subtitle = QLabel(
            "Basculez les bits ou saisissez directement en Binaire, Décimal ou Hexadécimal. "
            "L'inspecteur vérifie en direct la validité du masque."
        )
        subtitle.setObjectName("tabSubtitle")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addWidget(header_card)

        # Main Converter Card
        card = QFrame()
        card.setObjectName("mainCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 16)
        card_layout.setSpacing(16)

        # 8-bit checkboxes row
        bits_layout = QHBoxLayout()
        bits_layout.setSpacing(10)

        for i, val in enumerate(self.bit_values):
            bit_box = QFrame()
            bit_box.setObjectName("bitBox")
            bit_box_layout = QVBoxLayout(bit_box)
            bit_box_layout.setContentsMargins(8, 8, 8, 8)
            bit_box_layout.setSpacing(5)
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
            bit_box_layout.addWidget(cb, alignment=Qt.AlignmentFlag.AlignCenter)
            bit_box_layout.addWidget(bit_pos)

            self.bit_cards.append(bit_box)
            bits_layout.addWidget(bit_box)

        card_layout.addLayout(bits_layout)

        # Multi-Format Interactive Input & Display Boxes
        inputs_layout = QHBoxLayout()
        inputs_layout.setSpacing(14)

        # 1. Binary Input Card
        bin_card = QFrame()
        bin_card.setObjectName("resultBox")
        bin_layout = QVBoxLayout(bin_card)
        bin_layout.setContentsMargins(12, 8, 12, 8)
        bin_title = QLabel("Binaire (8-bit)")
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
        dec_layout.setContentsMargins(12, 8, 12, 8)
        dec_title = QLabel("Décimal (0 - 255)")
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
        hex_layout.setContentsMargins(12, 8, 12, 8)
        hex_title = QLabel("Hexadécimal (00 - FF)")
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
        controls_layout.setSpacing(8)

        quick_label = QLabel("Presets Rapides :")
        quick_label.setObjectName("inputLabel")

        btn_all_on = QPushButton("All 1s (255)")
        btn_all_on.setObjectName("toolBtn")
        btn_all_on.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_all_on.clicked.connect(self.set_all_ones)

        btn_clear = QPushButton("Clear All (0)")
        btn_clear.setObjectName("toolBtn")
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.clicked.connect(self.clear_all)

        btn_invert = QPushButton("Inverser (~X)")
        btn_invert.setObjectName("toolBtn")
        btn_invert.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_invert.clicked.connect(self.invert_bits)

        controls_layout.addWidget(quick_label)
        controls_layout.addWidget(btn_all_on)
        controls_layout.addWidget(btn_clear)
        controls_layout.addWidget(btn_invert)

        # Common mask presets
        for mask_val in (128, 192, 224, 240, 248, 252):
            btn_m = QPushButton(str(mask_val))
            btn_m.setObjectName("presetBtn")
            btn_m.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_m.clicked.connect(lambda _checked, v=mask_val: self.apply_value(v, source="preset"))
            controls_layout.addWidget(btn_m)

        controls_layout.addStretch()
        card_layout.addLayout(controls_layout)
        layout.addWidget(card)

        # Compact Read-Only Mask & Complement Inspector Bar (v1.2.0)
        inspector_card = QFrame()
        inspector_card.setObjectName("inspectorCard")
        insp_layout = QHBoxLayout(inspector_card)
        insp_layout.setContentsMargins(18, 12, 18, 12)
        insp_layout.setSpacing(20)

        # 1. Valid Mask Octet?
        col1 = QVBoxLayout()
        lbl_m_title = QLabel("OCTET DE MASQUE VALIDE ?")
        lbl_m_title.setObjectName("resultTitle")
        self.lbl_valid_mask = QLabel("Oui (bits contigus)")
        self.lbl_valid_mask.setObjectName("inspectorValueValid")
        col1.addWidget(lbl_m_title)
        col1.addWidget(self.lbl_valid_mask)

        # 2. One's Complement (~X)
        col2 = QVBoxLayout()
        lbl_c_title = QLabel("COMPLÉMENT À 1 (~X = 255 − X)")
        lbl_c_title.setObjectName("resultTitle")
        self.lbl_complement = QLabel("255  (11111111)")
        self.lbl_complement.setObjectName("inspectorValueMono")
        col2.addWidget(lbl_c_title)
        col2.addWidget(self.lbl_complement)

        # 3. Subnet Block Step (256 - X)
        col3 = QVBoxLayout()
        lbl_s_title = QLabel("PAS DU SOUS-RÉSEAU (256 − X)")
        lbl_s_title.setObjectName("resultTitle")
        self.lbl_block_step = QLabel("256")
        self.lbl_block_step.setObjectName("inspectorValueMono")
        col3.addWidget(lbl_s_title)
        col3.addWidget(self.lbl_block_step)

        insp_layout.addLayout(col1, stretch=1)
        insp_layout.addLayout(col2, stretch=1)
        insp_layout.addLayout(col3, stretch=1)

        layout.addWidget(inspector_card)
        layout.addStretch()

        self.apply_value(0, source="init")

    def apply_value(self, val: int, source: str = ""):
        """Central update method synchronizing bit cards, inputs, and mask inspector."""
        analysis = IPv4MathEngine.analyze_octet(val)
        self.current_value = analysis.value

        self._updating = True
        try:
            for i, bit_val in enumerate(self.bit_values):
                is_on = bool(analysis.value & bit_val)
                if self.checkboxes[i].isChecked() != is_on:
                    self.checkboxes[i].setChecked(is_on)
                self.bit_cards[i].setProperty("active", is_on)
                self.bit_cards[i].style().unpolish(self.bit_cards[i])
                self.bit_cards[i].style().polish(self.bit_cards[i])

            if source != "binary":
                self.bin_input.setText(analysis.binary_str)
            if source != "decimal":
                self.dec_input.setText(str(analysis.value))
            if source != "hex":
                self.hex_input.setText(analysis.hex_str)

            # Update Mask & Complement Inspector
            if analysis.is_valid_mask_octet:
                self.lbl_valid_mask.setText("Oui (bits à 1 contigus)")
                self.lbl_valid_mask.setObjectName("inspectorValueValid")
            else:
                self.lbl_valid_mask.setText("Non (1 et 0 alternés)")
                self.lbl_valid_mask.setObjectName("inspectorValueInvalid")
            self.lbl_valid_mask.style().unpolish(self.lbl_valid_mask)
            self.lbl_valid_mask.style().polish(self.lbl_valid_mask)

            self.lbl_complement.setText(
                f"{analysis.ones_complement}  ({analysis.ones_complement_binary})"
            )
            self.lbl_block_step.setText(
                f"{analysis.block_size}  (Magic Number)"
                if analysis.is_valid_mask_octet and analysis.value > 0
                else str(analysis.block_size)
            )
        finally:
            self._updating = False

    def on_checkbox_toggled(self):
        if self._updating:
            return
        total = sum(
            self.bit_values[i]
            for i, cb in enumerate(self.checkboxes)
            if cb.isChecked()
        )
        self.apply_value(total, source="checkbox")

    def on_binary_edited(self, text: str):
        if self._updating:
            return
        cleaned = text.replace(" ", "").replace("_", "")
        filtered = "".join([c for c in cleaned if c in "01"])[:8]
        val = int(filtered, 2) if filtered else 0
        self.apply_value(val, source="binary")

    def on_decimal_edited(self, text: str):
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

    def on_hex_edited(self, text: str):
        if self._updating:
            return
        cleaned = text.strip().lower()
        if cleaned.startswith("0x"):
            cleaned = cleaned[2:]
        cleaned = "".join([c for c in cleaned if c in "0123456789abcdef"])[:2]
        val = int(cleaned, 16) if cleaned else 0
        self.apply_value(val, source="hex")

    def set_all_ones(self):
        self.apply_value(255, source="preset")

    def clear_all(self):
        self.apply_value(0, source="preset")

    def invert_bits(self):
        self.apply_value(IPv4MathEngine.ones_complement_octet(self.current_value), source="preset")
