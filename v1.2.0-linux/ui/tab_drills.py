"""
ui/tab_drills.py
Tab 4: Flash Drills — Express Course Mini-Exercises:
1. Fragmentation MTU (Total Length, IHL, MTU -> Payload, Offset /8, MF Flag)
2. Routage LPM (Routing table of 4 routes -> Winning route & Decisive rule)
3. Checksum Hexa (16-bit header words -> Raw sum, End-around carry sum, One's complement)
"""

from typing import Callable, Dict, List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QStackedWidget, QLabel, QLineEdit, QPushButton, QFrame
)
from PyQt6.QtCore import Qt

from engine.drills_solver import (
    ChecksumProblem, DrillsSolver, LpmProblem, MtuProblem
)


class FlashDrillsTab(QWidget):
    """Tab 4: Flash Drills with a single active drill view at a time for zero clutter."""

    def __init__(self, on_clean_solve: Optional[Callable[[str], None]] = None):
        super().__init__()
        self.on_clean_solve = on_clean_solve

        # State for Drill 1 (MTU)
        self.current_mtu: Optional[MtuProblem] = None
        self.mtu_payload_inputs: List[QLineEdit] = []
        self.mtu_offset_inputs: List[QLineEdit] = []
        self.mtu_mf_inputs: List[QLineEdit] = []
        self.mtu_status_labels: List[QLabel] = []
        self.mtu_used_show = False
        self.mtu_rewarded = False
        self.mtu_shown_state = False

        # State for Drill 2 (LPM)
        self.current_lpm: Optional[LpmProblem] = None
        self.lpm_route_labels: List[List[QLabel]] = []
        self.lpm_route_btns: Dict[int, QPushButton] = {}
        self.lpm_rule_btns: Dict[str, QPushButton] = {}
        self.selected_route_id: Optional[int] = None
        self.selected_rule: Optional[str] = None
        self.lpm_used_show = False
        self.lpm_rewarded = False

        # State for Drill 3 (Checksum)
        self.current_chk: Optional[ChecksumProblem] = None
        self.chk_used_show = False
        self.chk_rewarded = False
        self.chk_shown_state = False

        self.init_ui()
        self.load_mtu_cours()
        self.load_lpm_problem("lpm")
        self.load_checksum_cours()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 14, 24, 14)
        main_layout.setSpacing(12)

        # Top Drill Selector Bar
        nav_card = QFrame()
        nav_card.setObjectName("headerCard")
        nav_layout = QHBoxLayout(nav_card)
        nav_layout.setContentsMargins(16, 10, 16, 10)
        nav_layout.setSpacing(12)

        lbl_mode = QLabel("Mini-Exercice :")
        lbl_mode.setObjectName("targetLabel")
        nav_layout.addWidget(lbl_mode)

        self.nav_buttons: List[QPushButton] = []
        titles = [
            "Fragmentation MTU",
            "Routage LPM && AD",
            "Checksum Hexa (16-bit)",
        ]
        for idx, text in enumerate(titles):
            btn = QPushButton(text)
            btn.setObjectName("drillNavBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _checked, i=idx: self.switch_drill(i))
            self.nav_buttons.append(btn)
            nav_layout.addWidget(btn)

        nav_layout.addStretch()
        main_layout.addWidget(nav_card)

        # Stacked Widget (Only 1 drill displayed at a time)
        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_mtu_page())
        self.stack.addWidget(self._build_lpm_page())
        self.stack.addWidget(self._build_checksum_page())
        main_layout.addWidget(self.stack)

        self.switch_drill(0)

    def switch_drill(self, idx: int):
        self.stack.setCurrentIndex(idx)
        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", i == idx)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    # ========================================================================
    # PAGE 1: MTU FRAGMENTATION
    # ========================================================================
    def _build_mtu_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        top_bar = QFrame()
        top_bar.setObjectName("topBarContainer")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(16, 10, 16, 10)
        top_layout.setSpacing(12)

        self.lbl_mtu_statement = QLabel("Paquet : Total Length = 4000 octets  |  IHL = 5  |  MTU = 1500 octets")
        self.lbl_mtu_statement.setObjectName("targetIpDisplay")

        btn_cours = QPushButton("Ex. Cours (4000B)")
        btn_cours.setObjectName("presetBtn")
        btn_cours.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cours.clicked.connect(self.load_mtu_cours)

        btn_rand = QPushButton("Nouveau Paquet")
        btn_rand.setObjectName("btnNextProblem")
        btn_rand.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_rand.clicked.connect(self.load_mtu_random)

        self.btn_mtu_show = QPushButton("Show")
        self.btn_mtu_show.setObjectName("btnShow")
        self.btn_mtu_show.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_mtu_show.clicked.connect(self.toggle_mtu_show)

        top_layout.addWidget(self.lbl_mtu_statement)
        top_layout.addStretch()
        top_layout.addWidget(btn_cours)
        top_layout.addWidget(btn_rand)
        top_layout.addWidget(self.btn_mtu_show)
        layout.addWidget(top_bar)

        # Formula Reminder Strip
        self.lbl_mtu_hint = QLabel(
            "Rappel : En-tête = IHL × 4  |  Données Max/Frag = ((MTU − En-tête) // 8) × 8  |  Offset = Octet_Début / 8"
        )
        self.lbl_mtu_hint.setObjectName("tabSubtitle")
        layout.addWidget(self.lbl_mtu_hint)

        # 3-Fragment Table
        table_card = QFrame()
        table_card.setObjectName("tableCard")
        grid = QGridLayout(table_card)
        grid.setContentsMargins(24, 16, 24, 18)
        grid.setHorizontalSpacing(22)
        grid.setVerticalSpacing(12)

        headers = [
            ("Fragment", 0),
            ("Données Utiles (octets)", 1),
            ("Offset (unités de 8 octets)", 2),
            ("Flag MF (0 ou 1)", 3),
            ("Correct?", 4),
        ]
        for text, col in headers:
            h_lbl = QLabel(text)
            h_lbl.setObjectName("columnHeader")
            h_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter if col > 0 else Qt.AlignmentFlag.AlignLeft)
            grid.addWidget(h_lbl, 0, col)

        for i in range(3):
            row_idx = i + 1
            lbl_f = QLabel(f"Fragment #{row_idx}")
            lbl_f.setObjectName("rowLabel")

            inp_pay = QLineEdit()
            inp_pay.setObjectName("subnetInput")
            inp_pay.setPlaceholderText("ex: 1480")
            inp_pay.setAlignment(Qt.AlignmentFlag.AlignCenter)
            inp_pay.textChanged.connect(lambda _t, r=i: self.validate_mtu_row(r))
            self.mtu_payload_inputs.append(inp_pay)

            inp_off = QLineEdit()
            inp_off.setObjectName("subnetInput")
            inp_off.setPlaceholderText("ex: 0, 185...")
            inp_off.setAlignment(Qt.AlignmentFlag.AlignCenter)
            inp_off.textChanged.connect(lambda _t, r=i: self.validate_mtu_row(r))
            self.mtu_offset_inputs.append(inp_off)

            inp_mf = QLineEdit()
            inp_mf.setObjectName("subnetInput")
            inp_mf.setPlaceholderText("1 ou 0")
            inp_mf.setAlignment(Qt.AlignmentFlag.AlignCenter)
            inp_mf.setFixedWidth(90)
            inp_mf.textChanged.connect(lambda _t, r=i: self.validate_mtu_row(r))
            self.mtu_mf_inputs.append(inp_mf)

            status = QLabel("✕")
            status.setObjectName("statusWrong")
            status.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.mtu_status_labels.append(status)

            grid.addWidget(lbl_f, row_idx, 0)
            grid.addWidget(inp_pay, row_idx, 1)
            grid.addWidget(inp_off, row_idx, 2)
            grid.addWidget(inp_mf, row_idx, 3, alignment=Qt.AlignmentFlag.AlignCenter)
            grid.addWidget(status, row_idx, 4)

        layout.addWidget(table_card)
        layout.addStretch()
        return page

    def load_mtu_cours(self):
        self._apply_mtu(DrillsSolver.preset_mtu_cours())

    def load_mtu_random(self):
        self._apply_mtu(DrillsSolver.generate_random_mtu())

    def _apply_mtu(self, prob: MtuProblem):
        self.current_mtu = prob
        self.mtu_used_show = False
        self.mtu_rewarded = False
        self.mtu_shown_state = False
        self.btn_mtu_show.setText("Show")

        self.lbl_mtu_statement.setText(
            f"Total Length = {prob.total_length} octets   |   IHL = {prob.ihl} ({prob.header_length}B)   |   MTU = {prob.mtu} octets"
        )

        for i in range(3):
            for w in (self.mtu_payload_inputs[i], self.mtu_offset_inputs[i], self.mtu_mf_inputs[i]):
                w.blockSignals(True)
                w.clear()
                w.blockSignals(False)
            self._set_status(self.mtu_status_labels[i], False)

    def validate_mtu_row(self, row_idx: int):
        if self.current_mtu is None or row_idx >= len(self.current_mtu.fragments):
            return
        frag = self.current_mtu.fragments[row_idx]
        p_txt = self.mtu_payload_inputs[row_idx].text().strip()
        o_txt = self.mtu_offset_inputs[row_idx].text().strip()
        m_txt = self.mtu_mf_inputs[row_idx].text().strip()

        is_ok = (
            p_txt.isdigit() and int(p_txt) == frag.payload_bytes
            and o_txt.isdigit() and int(o_txt) == frag.offset_units
            and m_txt.isdigit() and int(m_txt) == frag.mf_flag
        )
        self._set_status(self.mtu_status_labels[row_idx], is_ok)

        if not self.mtu_rewarded and not self.mtu_used_show:
            if all(lbl.text() == "✓" for lbl in self.mtu_status_labels):
                self.mtu_rewarded = True
                if self.on_clean_solve:
                    self.on_clean_solve("mtu_clean")

    def toggle_mtu_show(self):
        if self.current_mtu is None:
            return
        self.mtu_used_show = True
        self.mtu_shown_state = not self.mtu_shown_state
        if self.mtu_shown_state:
            for i, frag in enumerate(self.current_mtu.fragments[:3]):
                self.mtu_payload_inputs[i].setText(str(frag.payload_bytes))
                self.mtu_offset_inputs[i].setText(str(frag.offset_units))
                self.mtu_mf_inputs[i].setText(str(frag.mf_flag))
            self.btn_mtu_show.setText("Hide")
        else:
            for i in range(3):
                self.mtu_payload_inputs[i].clear()
                self.mtu_offset_inputs[i].clear()
                self.mtu_mf_inputs[i].clear()
            self.btn_mtu_show.setText("Show")

    # ========================================================================
    # PAGE 2: ROUTING & LONGEST PREFIX MATCH (LPM)
    # ========================================================================
    def _build_lpm_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        top_bar = QFrame()
        top_bar.setObjectName("topBarContainer")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(16, 8, 16, 8)
        top_layout.setSpacing(10)

        lbl_d = QLabel("Paquet à router vers l'IP Destination :")
        lbl_d.setObjectName("targetLabel")

        self.lbl_lpm_dest = QLabel("192.168.12.45")
        self.lbl_lpm_dest.setObjectName("targetIpDisplay")

        top_layout.addWidget(lbl_d)
        top_layout.addWidget(self.lbl_lpm_dest)
        top_layout.addStretch()

        for code, label in [("lpm", "Cas LPM"), ("ad", "Cas AD"), ("metric", "Cas Métrique"), ("random", "Aléatoire")]:
            btn = QPushButton(label)
            btn.setObjectName("btnNextProblem" if code == "random" else "presetBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _c, sc=code: self.load_lpm_problem(sc))
            top_layout.addWidget(btn)

        self.btn_lpm_show = QPushButton("Show")
        self.btn_lpm_show.setObjectName("btnShow")
        self.btn_lpm_show.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_lpm_show.clicked.connect(self.show_lpm_solution)
        top_layout.addWidget(self.btn_lpm_show)

        layout.addWidget(top_bar)

        # Routing Table Card (4 rows)
        table_card = QFrame()
        table_card.setObjectName("tableCard")
        grid = QGridLayout(table_card)
        grid.setContentsMargins(20, 12, 20, 12)
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(8)

        headers = ["Route", "Code Protocole", "Destination / CIDR", "[AD / Métrique]", "Next Hop", "Interface"]
        for col, h_text in enumerate(headers):
            h_lbl = QLabel(h_text)
            h_lbl.setObjectName("columnHeader")
            grid.addWidget(h_lbl, 0, col)

        for r in range(4):
            row_widgets: List[QLabel] = []
            for c in range(6):
                lbl = QLabel("")
                lbl.setObjectName("monoDetailLabel")
                grid.addWidget(lbl, r + 1, c)
                row_widgets.append(lbl)
            self.lpm_route_labels.append(row_widgets)

        layout.addWidget(table_card)

        # User Decision Card
        decision_card = QFrame()
        decision_card.setObjectName("inspectorCard")
        dec_layout = QVBoxLayout(decision_card)
        dec_layout.setContentsMargins(16, 10, 16, 10)
        dec_layout.setSpacing(8)

        # Row 1: Winning Route Selection
        r1 = QHBoxLayout()
        lbl_q1 = QLabel("1. Route choisie par le routeur :")
        lbl_q1.setObjectName("inputLabel")
        r1.addWidget(lbl_q1)

        for r_id in (1, 2, 3, 4):
            btn = QPushButton(f"Route #{r_id}")
            btn.setObjectName("choiceBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _c, rid=r_id: self.on_select_lpm_route(rid))
            self.lpm_route_btns[r_id] = btn
            r1.addWidget(btn)

        self.lbl_lpm_route_status = QLabel("✕")
        self.lbl_lpm_route_status.setObjectName("statusWrong")
        r1.addWidget(self.lbl_lpm_route_status)
        r1.addStretch()
        dec_layout.addLayout(r1)

        # Row 2: Decisive Rule Selection
        r2 = QHBoxLayout()
        lbl_q2 = QLabel("2. Règle décisive appliquée :")
        lbl_q2.setObjectName("inputLabel")
        r2.addWidget(lbl_q2)

        rules = [
            "Longest Prefix Match",
            "Distance Administrative (AD)",
            "Métrique",
            "Route par défaut",
        ]
        for rule_name in rules:
            btn = QPushButton(rule_name)
            btn.setObjectName("choiceBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _c, rn=rule_name: self.on_select_lpm_rule(rn))
            self.lpm_rule_btns[rule_name] = btn
            r2.addWidget(btn)

        self.lbl_lpm_rule_status = QLabel("✕")
        self.lbl_lpm_rule_status.setObjectName("statusWrong")
        r2.addWidget(self.lbl_lpm_rule_status)
        r2.addStretch()
        dec_layout.addLayout(r2)

        self.lbl_lpm_explanation = QLabel("")
        self.lbl_lpm_explanation.setObjectName("tabSubtitle")
        self.lbl_lpm_explanation.setWordWrap(True)
        dec_layout.addWidget(self.lbl_lpm_explanation)

        layout.addWidget(decision_card)
        layout.addStretch()
        return page

    def load_lpm_problem(self, scenario: str = "random"):
        prob = DrillsSolver.generate_lpm_problem(scenario)
        self.current_lpm = prob
        self.lpm_used_show = False
        self.lpm_rewarded = False
        self.selected_route_id = None
        self.selected_rule = None

        self.lbl_lpm_dest.setText(prob.destination_ip)
        self.lbl_lpm_explanation.setText("Sélectionnez la route gagnante et la règle qui a tranché.")

        proto_names = {"C": "C (Connecté)", "S": "S (Statique)", "O": "O (OSPF)", "R": "R (RIP)", "S*": "S* (Défaut)"}
        for idx, route in enumerate(prob.routes):
            vals = [
                f"#{route.row_id}",
                proto_names.get(route.protocol_code, route.protocol_code),
                route.network_prefix,
                route.bracket_str,
                route.next_hop,
                route.interface,
            ]
            for c, val in enumerate(vals):
                self.lpm_route_labels[idx][c].setText(val)

        for btn in self.lpm_route_btns.values():
            btn.setProperty("selected", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        for btn in self.lpm_rule_btns.values():
            btn.setProperty("selected", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        self._set_status(self.lbl_lpm_route_status, False)
        self._set_status(self.lbl_lpm_rule_status, False)

    def on_select_lpm_route(self, route_id: int):
        self.selected_route_id = route_id
        for rid, btn in self.lpm_route_btns.items():
            btn.setProperty("selected", rid == route_id)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        is_ok = (self.current_lpm is not None and route_id == self.current_lpm.winning_row_id)
        self._set_status(self.lbl_lpm_route_status, is_ok)
        self._check_lpm_complete()

    def on_select_lpm_rule(self, rule_name: str):
        self.selected_rule = rule_name
        for rname, btn in self.lpm_rule_btns.items():
            btn.setProperty("selected", rname == rule_name)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        is_ok = (self.current_lpm is not None and rule_name == self.current_lpm.decisive_rule)
        self._set_status(self.lbl_lpm_rule_status, is_ok)
        self._check_lpm_complete()

    def _check_lpm_complete(self):
        if self.current_lpm is None:
            return
        if self.lbl_lpm_route_status.text() == "✓" and self.lbl_lpm_rule_status.text() == "✓":
            self.lbl_lpm_explanation.setText(f"Explication : {self.current_lpm.explanation}")
            if not self.lpm_rewarded and not self.lpm_used_show:
                self.lpm_rewarded = True
                if self.on_clean_solve:
                    self.on_clean_solve("lpm_clean")

    def show_lpm_solution(self):
        if self.current_lpm is None:
            return
        self.lpm_used_show = True
        self.on_select_lpm_route(self.current_lpm.winning_row_id)
        self.on_select_lpm_rule(self.current_lpm.decisive_rule)

    # ========================================================================
    # PAGE 3: IPV4 16-BIT HEADER CHECKSUM
    # ========================================================================
    def _build_checksum_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        top_bar = QFrame()
        top_bar.setObjectName("topBarContainer")
        top_vbox = QVBoxLayout(top_bar)
        top_vbox.setContentsMargins(18, 10, 18, 10)
        top_vbox.setSpacing(8)

        row1 = QHBoxLayout()
        lbl_t = QLabel("Mots de 16 bits de l'en-tête IPv4 (Hexadécimal) :")
        lbl_t.setObjectName("targetLabel")

        btn_cours = QPushButton("Ex. Cours 10 mots")
        btn_cours.setObjectName("presetBtn")
        btn_cours.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cours.clicked.connect(self.load_checksum_cours)

        btn_short = QPushButton("Mode Court (4 mots)")
        btn_short.setObjectName("btnNextProblem")
        btn_short.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_short.clicked.connect(self.load_checksum_short)

        self.btn_chk_show = QPushButton("Show")
        self.btn_chk_show.setObjectName("btnShow")
        self.btn_chk_show.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_chk_show.clicked.connect(self.toggle_checksum_show)

        row1.addWidget(lbl_t)
        row1.addStretch()
        row1.addWidget(btn_cours)
        row1.addWidget(btn_short)
        row1.addWidget(self.btn_chk_show)

        self.lbl_chk_words = QLabel("  4500   0054   0000   4000   4001   0000   C0A8   0068   C0A8   0001  ")
        self.lbl_chk_words.setObjectName("targetIpDisplay")
        self.lbl_chk_words.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_vbox.addLayout(row1)
        top_vbox.addWidget(self.lbl_chk_words)
        layout.addWidget(top_bar)

        # 3-Step Checksum Calculation Card
        card = QFrame()
        card.setObjectName("tableCard")
        grid = QGridLayout(card)
        grid.setContentsMargins(24, 18, 24, 18)
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(14)

        steps = [
            ("Étape 1 — Somme hexadécimale brute (ex: 0x2470E)", "raw"),
            ("Étape 2 — Après rabattement de la retenue (End-Around Carry 16 bits)", "carried"),
            ("Étape 3 — Complément à un final (~Somme & 0xFFFF = Checksum)", "final"),
        ]

        self.chk_inputs: Dict[str, QLineEdit] = {}
        self.chk_status: Dict[str, QLabel] = {}

        for idx, (label_text, key) in enumerate(steps):
            lbl = QLabel(label_text)
            lbl.setObjectName("rowLabel")

            inp = QLineEdit()
            inp.setObjectName("subnetInput")
            inp.setPlaceholderText("0x....")
            inp.setAlignment(Qt.AlignmentFlag.AlignCenter)
            inp.setFixedWidth(180)
            inp.textChanged.connect(self.validate_checksum)
            self.chk_inputs[key] = inp

            st = QLabel("✕")
            st.setObjectName("statusWrong")
            st.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.chk_status[key] = st

            grid.addWidget(lbl, idx, 0)
            grid.addWidget(inp, idx, 1)
            grid.addWidget(st, idx, 2)

        layout.addWidget(card)
        layout.addStretch()
        return page

    def load_checksum_cours(self):
        self._apply_checksum(DrillsSolver.preset_checksum_cours())

    def load_checksum_short(self):
        self._apply_checksum(DrillsSolver.generate_short_checksum())

    def _apply_checksum(self, prob: ChecksumProblem):
        self.current_chk = prob
        self.chk_used_show = False
        self.chk_rewarded = False
        self.chk_shown_state = False
        self.btn_chk_show.setText("Show")

        self.lbl_chk_words.setText("  " + "   ".join(prob.words_hex) + "  ")
        for k, inp in self.chk_inputs.items():
            inp.blockSignals(True)
            inp.clear()
            inp.blockSignals(False)
            self._set_status(self.chk_status[k], False)

    def validate_checksum(self):
        if self.current_chk is None:
            return
        raw_val = DrillsSolver.parse_hex_input(self.chk_inputs["raw"].text())
        car_val = DrillsSolver.parse_hex_input(self.chk_inputs["carried"].text())
        fin_val = DrillsSolver.parse_hex_input(self.chk_inputs["final"].text())

        raw_ok = (raw_val == self.current_chk.raw_sum)
        car_ok = (car_val == self.current_chk.carried_sum)
        fin_ok = (fin_val == self.current_chk.checksum)

        self._set_status(self.chk_status["raw"], raw_ok)
        self._set_status(self.chk_status["carried"], car_ok)
        self._set_status(self.chk_status["final"], fin_ok)

        if raw_ok and car_ok and fin_ok and not self.chk_rewarded and not self.chk_used_show:
            self.chk_rewarded = True
            if self.on_clean_solve:
                self.on_clean_solve("checksum_clean")

    def toggle_checksum_show(self):
        if self.current_chk is None:
            return
        self.chk_used_show = True
        self.chk_shown_state = not self.chk_shown_state
        if self.chk_shown_state:
            self.chk_inputs["raw"].setText(self.current_chk.raw_sum_hex)
            self.chk_inputs["carried"].setText(self.current_chk.carried_sum_hex)
            self.chk_inputs["final"].setText(self.current_chk.checksum_hex)
            self.btn_chk_show.setText("Hide")
        else:
            for inp in self.chk_inputs.values():
                inp.clear()
            self.btn_chk_show.setText("Show")

    def _set_status(self, lbl: QLabel, is_ok: bool):
        if is_ok:
            lbl.setText("✓")
            lbl.setObjectName("statusCorrect")
        else:
            lbl.setText("✕")
            lbl.setObjectName("statusWrong")
        lbl.style().unpolish(lbl)
        lbl.style().polish(lbl)
