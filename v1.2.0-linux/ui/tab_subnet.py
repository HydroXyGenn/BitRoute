"""
ui/tab_subnet.py
Tab 2: Subnet Practice + Class/Scope Quick Selectors + Collapsible 32-Bit Binary Drawer.
"""

from typing import Callable, Dict, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QFrame
)
from PyQt6.QtCore import Qt

from engine.ipv4_math import IPv4MathEngine, SubnetAnalysis
from ui.widgets import IpLineEdit


class SubnetPracticeTab(QWidget):
    """Tab 2: Subnet Practice with Class/Scope classification and progressive 32-bit binary drawer."""

    def __init__(self, on_clean_solve: Optional[Callable[[str], None]] = None):
        super().__init__()
        self.on_clean_solve = on_clean_solve
        self.current_analysis: Optional[SubnetAnalysis] = None
        self.answers: Dict[str, str] = {}

        self.input_fields: Dict[str, IpLineEdit] = {}
        self.status_labels: Dict[str, QLabel] = {}
        self.answer_fields: Dict[str, QLineEdit] = {}
        self.show_buttons: Dict[str, QPushButton] = {}
        self.answer_visible: Dict[str, bool] = {}

        self.selected_class: Optional[str] = None
        self.selected_type: Optional[str] = None
        self.class_buttons: Dict[str, QPushButton] = {}
        self.type_buttons: Dict[str, QPushButton] = {}

        self.used_show_on_current = False
        self.rewarded_current = False

        self.init_ui()
        self.generate_new_problem()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 14, 24, 14)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ----------------- Top Header Bar -----------------
        top_bar_container = QFrame()
        top_bar_container.setObjectName("topBarContainer")
        top_bar_layout = QHBoxLayout(top_bar_container)
        top_bar_layout.setContentsMargins(18, 8, 18, 8)
        top_bar_layout.setSpacing(10)
        top_bar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        target_label = QLabel("Target IP address")
        target_label.setObjectName("targetLabel")

        self.ip_display = QLabel("104 . 172 . 78 . 239")
        self.ip_display.setObjectName("targetIpDisplay")
        self.ip_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        slash_label = QLabel("/")
        slash_label.setObjectName("slashLabel")

        self.cidr_display = QLabel("23")
        self.cidr_display.setObjectName("targetCidrDisplay")
        self.cidr_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_cours = QPushButton("Ex. Cours (154.4.32.0/19)")
        self.btn_cours.setObjectName("presetBtn")
        self.btn_cours.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cours.clicked.connect(self.load_course_example)

        self.btn_next = QPushButton("Next Problem")
        self.btn_next.setObjectName("btnNextProblem")
        self.btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_next.clicked.connect(self.generate_new_problem)

        top_bar_layout.addWidget(target_label)
        top_bar_layout.addWidget(self.ip_display)
        top_bar_layout.addWidget(slash_label)
        top_bar_layout.addWidget(self.cidr_display)
        top_bar_layout.addSpacing(6)
        top_bar_layout.addWidget(self.btn_cours)
        top_bar_layout.addWidget(self.btn_next)

        main_layout.addWidget(top_bar_container, alignment=Qt.AlignmentFlag.AlignCenter)

        # ----------------- Quick Class & Type Selector Bar -----------------
        classif_card = QFrame()
        classif_card.setObjectName("headerCard")
        classif_layout = QHBoxLayout(classif_card)
        classif_layout.setContentsMargins(16, 8, 16, 8)
        classif_layout.setSpacing(10)

        lbl_cls = QLabel("Classe :")
        lbl_cls.setObjectName("inputLabel")
        classif_layout.addWidget(lbl_cls)

        for c_name in ("A", "B", "C"):
            btn = QPushButton(c_name)
            btn.setObjectName("choiceBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _checked, c=c_name: self.on_select_class(c))
            self.class_buttons[c_name] = btn
            classif_layout.addWidget(btn)

        self.lbl_class_status = QLabel("✕")
        self.lbl_class_status.setObjectName("statusWrong")
        classif_layout.addWidget(self.lbl_class_status)

        classif_layout.addSpacing(20)

        lbl_typ = QLabel("Type :")
        lbl_typ.setObjectName("inputLabel")
        classif_layout.addWidget(lbl_typ)

        for t_name in ("Publique", "Privée", "APIPA", "Loopback"):
            btn = QPushButton(t_name)
            btn.setObjectName("choiceBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _checked, t=t_name: self.on_select_type(t))
            self.type_buttons[t_name] = btn
            classif_layout.addWidget(btn)

        self.lbl_type_status = QLabel("✕")
        self.lbl_type_status.setObjectName("statusWrong")
        classif_layout.addWidget(self.lbl_type_status)
        classif_layout.addStretch()

        main_layout.addWidget(classif_card)

        # ----------------- Main 5-Row Subnet Table Card -----------------
        table_card = QFrame()
        table_card.setObjectName("tableCard")
        grid = QGridLayout(table_card)
        grid.setContentsMargins(24, 14, 24, 16)
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(10)

        headers = [("IP address", 1), ("Correct?", 2), ("Answer", 3), ("Show", 4)]
        for text, col in headers:
            h_lbl = QLabel(text)
            h_lbl.setObjectName("columnHeader")
            h_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grid.addWidget(h_lbl, 0, col)

        self.row_keys = ["Network", "First Host", "Last Host", "Broadcast", "Next Subnet"]

        for row_idx, key in enumerate(self.row_keys, start=1):
            lbl_name = QLabel(key)
            lbl_name.setObjectName("rowLabel")
            lbl_name.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

            inp = IpLineEdit()
            inp.setObjectName("subnetInput")
            inp.setPlaceholderText(".     .     .")
            inp.setAlignment(Qt.AlignmentFlag.AlignCenter)
            inp.setMinimumWidth(185)
            inp.setMaximumWidth(215)
            inp.textChanged.connect(lambda _text, k=key: self.validate_input(k))
            self.input_fields[key] = inp

            status = QLabel("✕")
            status.setObjectName("statusWrong")
            status.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.status_labels[key] = status

            ans = QLineEdit()
            ans.setObjectName("answerField")
            ans.setReadOnly(True)
            ans.setPlaceholderText(".     .     .")
            ans.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ans.setMinimumWidth(185)
            ans.setMaximumWidth(215)
            self.answer_fields[key] = ans
            self.answer_visible[key] = False

            btn_show = QPushButton("Show")
            btn_show.setObjectName("btnShow")
            btn_show.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_show.clicked.connect(lambda _checked, k=key: self.toggle_show_answer(k))
            self.show_buttons[key] = btn_show

            grid.addWidget(lbl_name, row_idx, 0)
            grid.addWidget(inp, row_idx, 1)
            grid.addWidget(status, row_idx, 2)
            grid.addWidget(ans, row_idx, 3)
            grid.addWidget(btn_show, row_idx, 4)

        main_layout.addWidget(table_card)

        # ----------------- Progressive Disclosure: 32-Bit Binary Drawer -----------------
        drawer_toggle_row = QHBoxLayout()
        self.btn_toggle_drawer = QPushButton("Afficher le détail binaire (32 bits)")
        self.btn_toggle_drawer.setObjectName("toolBtn")
        self.btn_toggle_drawer.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle_drawer.clicked.connect(self.toggle_binary_drawer)
        drawer_toggle_row.addWidget(self.btn_toggle_drawer)
        drawer_toggle_row.addStretch()
        main_layout.addLayout(drawer_toggle_row)

        self.drawer_card = QFrame()
        self.drawer_card.setObjectName("drawerCard")
        self.drawer_card.setVisible(False)
        drawer_layout = QVBoxLayout(self.drawer_card)
        drawer_layout.setContentsMargins(18, 12, 18, 12)
        drawer_layout.setSpacing(6)

        self.lbl_drawer_lines = QLabel("")
        self.lbl_drawer_lines.setObjectName("monoDetailLabel")
        self.lbl_drawer_lines.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        drawer_layout.addWidget(self.lbl_drawer_lines)

        main_layout.addWidget(self.drawer_card)
        main_layout.addStretch()

    def load_course_example(self):
        """Loads the official INPT course example: 154.4.32.0/19."""
        analysis = IPv4MathEngine.analyze_subnet("154.4.32.0", 19)
        self._apply_problem(analysis)

    def generate_new_problem(self):
        """Generates a balanced random IPv4 subnetting problem via IPv4MathEngine."""
        analysis = IPv4MathEngine.generate_practice_problem()
        self._apply_problem(analysis)

    def _apply_problem(self, analysis: SubnetAnalysis):
        self.current_analysis = analysis
        self.used_show_on_current = False
        self.rewarded_current = False

        self.answers = {
            "Network": analysis.network_str,
            "First Host": analysis.first_host_str,
            "Last Host": analysis.last_host_str,
            "Broadcast": analysis.broadcast_str,
            "Next Subnet": analysis.next_subnet_str,
        }

        octets = analysis.ip_str.split(".")
        self.ip_display.setText(f"{octets[0]}  .  {octets[1]}  .  {octets[2]}  .  {octets[3]}")
        self.cidr_display.setText(str(analysis.cidr))

        # Reset Class & Type selectors
        self.selected_class = None
        self.selected_type = None
        for btn in self.class_buttons.values():
            btn.setProperty("selected", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        for btn in self.type_buttons.values():
            btn.setProperty("selected", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        self._set_status_label(self.lbl_class_status, False)
        self._set_status_label(self.lbl_type_status, False)

        # Reset 5-row table
        for key in self.row_keys:
            self.input_fields[key].blockSignals(True)
            self.input_fields[key].clear()
            self.input_fields[key].blockSignals(False)
            self._set_status_label(self.status_labels[key], False)
            self.answer_visible[key] = False
            self.answer_fields[key].setText("")
            self.show_buttons[key].setText("Show")

        # Update 32-bit binary drawer text
        def_cidr_str = f"/{analysis.default_class_cidr}" if analysis.default_class_cidr else "N/A"
        drawer_text = (
            f"IP Cible       ({analysis.ip_str:<15}) : {analysis.ip_bin_dotted}\n"
            f"Masque /{analysis.cidr:<2}     ({analysis.mask_str:<15}) : {analysis.mask_bin_dotted}\n"
            f"IP ET Masque   (Network  = {analysis.network_str:<15}) : {analysis.network_bin_dotted}\n"
            f"IP ET ~Masque  (Host ID  = {analysis.internal_host_id_str:<15}) : {analysis.host_id_bin_dotted}\n"
            f"──────────────────────────────────────────────────────────────────────────────────────\n"
            f"• Classe {analysis.ip_class} (bits de poids fort {analysis.leading_bits_pattern}, masque par défaut {def_cidr_str})  |  Portée : {analysis.address_type}\n"
            f"• Bits empruntés : b_S = {analysis.cidr} − {analysis.default_class_cidr} = {analysis.borrowed_bits} bits  →  2^{analysis.borrowed_bits} = {analysis.num_subnets_from_class} sous-réseau(x)\n"
            f"• Bits d'hôtes   : b_H = 32 − {analysis.cidr} = {analysis.host_bits} bits  →  2^{analysis.host_bits} − 2 = {analysis.usable_hosts} hôtes disponibles"
        )
        self.lbl_drawer_lines.setText(drawer_text)

    def _set_status_label(self, lbl: QLabel, is_correct: bool):
        if is_correct:
            lbl.setText("✓")
            lbl.setObjectName("statusCorrect")
        else:
            lbl.setText("✕")
            lbl.setObjectName("statusWrong")
        lbl.style().unpolish(lbl)
        lbl.style().polish(lbl)

    def on_select_class(self, c_name: str):
        self.selected_class = c_name
        for k, btn in self.class_buttons.items():
            btn.setProperty("selected", k == c_name)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        is_ok = (self.current_analysis is not None and c_name == self.current_analysis.ip_class)
        self._set_status_label(self.lbl_class_status, is_ok)
        self._check_all_solved()

    def on_select_type(self, t_name: str):
        self.selected_type = t_name
        for k, btn in self.type_buttons.items():
            btn.setProperty("selected", k == t_name)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        is_ok = (self.current_analysis is not None and t_name == self.current_analysis.address_type)
        self._set_status_label(self.lbl_type_status, is_ok)
        self._check_all_solved()

    def validate_input(self, key: str):
        user_raw = self.input_fields[key].text()
        normalized_user = IPv4MathEngine.normalize_ip_input(user_raw)
        correct_val = self.answers.get(key, "")

        is_ok = (normalized_user == correct_val)
        self._set_status_label(self.status_labels[key], is_ok)
        self._check_all_solved()

    def toggle_show_answer(self, key: str):
        self.used_show_on_current = True
        self.answer_visible[key] = not self.answer_visible[key]
        if self.answer_visible[key]:
            self.answer_fields[key].setText(self.answers.get(key, ""))
            self.show_buttons[key].setText("Hide")
        else:
            self.answer_fields[key].setText("")
            self.show_buttons[key].setText("Show")

    def toggle_binary_drawer(self):
        vis = self.drawer_card.isHidden()
        self.drawer_card.setVisible(vis)
        if vis:
            self.btn_toggle_drawer.setText("Masquer le détail binaire (32 bits)")
        else:
            self.btn_toggle_drawer.setText("Afficher le détail binaire (32 bits)")

    def _check_all_solved(self):
        if self.rewarded_current or self.used_show_on_current or self.current_analysis is None:
            return
        rows_ok = all(self.status_labels[k].text() == "✓" for k in self.row_keys)
        class_ok = (self.lbl_class_status.text() == "✓")
        type_ok = (self.lbl_type_status.text() == "✓")
        if rows_ok and class_ok and type_ok:
            self.rewarded_current = True
            if self.on_clean_solve:
                self.on_clean_solve("subnet_clean")
