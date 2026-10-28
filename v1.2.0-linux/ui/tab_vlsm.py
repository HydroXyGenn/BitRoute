"""
ui/tab_vlsm.py
Tab 3: VLSM Express Lab — Minimal decision inputs (Sorted Host Need, /CIDR, Network IP)
with instant auto-completion of Host Range, Broadcast, and Subnet Mask.
"""

from typing import Callable, Dict, List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt

from engine.ipv4_math import IPv4MathEngine
from engine.vlsm_solver import VlsmProblem, VlsmSolver
from ui.widgets import IpLineEdit


class VlsmLabTab(QWidget):
    """Tab 3: VLSM Express Workshop with anti-saturation auto-completion."""

    def __init__(self, on_clean_solve: Optional[Callable[[str], None]] = None):
        super().__init__()
        self.on_clean_solve = on_clean_solve
        self.current_problem: Optional[VlsmProblem] = None

        self.need_inputs: List[QLineEdit] = []
        self.cidr_inputs: List[QLineEdit] = []
        self.net_inputs: List[IpLineEdit] = []
        self.status_labels: List[QLabel] = []
        self.summary_badges: List[QLabel] = []
        self.show_buttons: List[QPushButton] = []
        self.row_shown: List[bool] = [False, False, False]

        self.used_show_on_current = False
        self.rewarded_current = False

        self.init_ui()
        self.load_preset_1()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 16, 24, 16)
        main_layout.setSpacing(14)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Header Card
        header_card = QFrame()
        header_card.setObjectName("headerCard")
        header_layout = QVBoxLayout(header_card)
        header_layout.setContentsMargins(18, 12, 18, 12)
        header_layout.setSpacing(4)

        title = QLabel("Atelier VLSM Express — Décision Pure & Auto-Complétion")
        title.setObjectName("tabTitle")
        subtitle = QLabel(
            "Règle d'Or : Triez les besoins du plus grand au plus petit (2^h − 2 ≥ N). "
            "Saisissez uniquement le Besoin, le /CIDR et l'Adresse Réseau : la plage et le Broadcast s'auto-complètent !"
        )
        subtitle.setObjectName("tabSubtitle")
        subtitle.setWordWrap(True)
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addWidget(header_card)

        # Top Problem Statement & Presets Bar
        top_bar = QFrame()
        top_bar.setObjectName("topBarContainer")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(16, 10, 16, 10)
        top_layout.setSpacing(10)

        lbl_base = QLabel("Réseau :")
        lbl_base.setObjectName("targetLabel")

        self.lbl_base_net = QLabel("193.225.34.0/24")
        self.lbl_base_net.setObjectName("targetIpDisplay")
        self.lbl_base_net.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_needs_title = QLabel("Besoins :")
        lbl_needs_title.setObjectName("targetLabel")

        self.lbl_unsorted_needs = QLabel("44 , 20 , 100")
        self.lbl_unsorted_needs.setObjectName("targetCidrDisplay")
        self.lbl_unsorted_needs.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout.addWidget(lbl_base)
        top_layout.addWidget(self.lbl_base_net)
        top_layout.addSpacing(10)
        top_layout.addWidget(lbl_needs_title)
        top_layout.addWidget(self.lbl_unsorted_needs)
        top_layout.addStretch()

        btn_c1 = QPushButton("Cours 1 (100, 44, 20)")
        btn_c1.setObjectName("presetBtn")
        btn_c1.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_c1.clicked.connect(self.load_preset_1)

        btn_c2 = QPushButton("Cours 2 (100, 28, 4)")
        btn_c2.setObjectName("presetBtn")
        btn_c2.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_c2.clicked.connect(self.load_preset_2)

        btn_rand = QPushButton("Nouveau VLSM")
        btn_rand.setObjectName("btnNextProblem")
        btn_rand.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_rand.clicked.connect(self.load_random_problem)

        top_layout.addWidget(btn_c1)
        top_layout.addWidget(btn_c2)
        top_layout.addWidget(btn_rand)

        main_layout.addWidget(top_bar)

        # 3-Row VLSM Allocation Table
        table_card = QFrame()
        table_card.setObjectName("tableCard")
        grid = QGridLayout(table_card)
        grid.setContentsMargins(20, 16, 20, 18)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(14)

        headers = [
            ("Sous-Réseau", 0),
            ("Besoin (N)", 1),
            ("/CIDR", 2),
            ("Adresse Réseau (Network IP)", 3),
            ("OK?", 4),
            ("Auto-Complétion (Plage d'hôtes, Broadcast & Masque)", 5),
            ("Aide", 6),
        ]
        for text, col in headers:
            h_lbl = QLabel(text)
            h_lbl.setObjectName("columnHeader")
            h_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter if col > 0 else Qt.AlignmentFlag.AlignLeft)
            grid.addWidget(h_lbl, 0, col)

        rank_labels = ["SR #1 (1er besoin)", "SR #2 (2ème besoin)", "SR #3 (3ème besoin)"]

        for i in range(3):
            row_idx = i + 1
            lbl_sr = QLabel(rank_labels[i])
            lbl_sr.setObjectName("rowLabel")

            inp_need = QLineEdit()
            inp_need.setObjectName("subnetInput")
            inp_need.setPlaceholderText("Nb hôtes")
            inp_need.setAlignment(Qt.AlignmentFlag.AlignCenter)
            inp_need.setFixedWidth(92)
            inp_need.textChanged.connect(lambda _t, r=i: self.validate_row(r))
            self.need_inputs.append(inp_need)

            inp_cidr = QLineEdit()
            inp_cidr.setObjectName("subnetInput")
            inp_cidr.setPlaceholderText("/25")
            inp_cidr.setAlignment(Qt.AlignmentFlag.AlignCenter)
            inp_cidr.setFixedWidth(74)
            inp_cidr.textChanged.connect(lambda _t, r=i: self.validate_row(r))
            self.cidr_inputs.append(inp_cidr)

            inp_net = IpLineEdit()
            inp_net.setObjectName("subnetInput")
            inp_net.setPlaceholderText(".   .   .")
            inp_net.setAlignment(Qt.AlignmentFlag.AlignCenter)
            inp_net.setFixedWidth(168)
            inp_net.textChanged.connect(lambda _t, r=i: self.validate_row(r))
            self.net_inputs.append(inp_net)

            lbl_status = QLabel("✕")
            lbl_status.setObjectName("statusWrong")
            lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_status.setFixedWidth(28)
            self.status_labels.append(lbl_status)

            lbl_summary = QLabel("Validez Besoin + /CIDR + Réseau...")
            lbl_summary.setObjectName("autoSummaryBadge")
            lbl_summary.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_summary.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.summary_badges.append(lbl_summary)

            btn_show = QPushButton("Show")
            btn_show.setObjectName("btnShow")
            btn_show.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_show.setFixedWidth(70)
            btn_show.clicked.connect(lambda _checked, r=i: self.toggle_show_row(r))
            self.show_buttons.append(btn_show)

            grid.addWidget(lbl_sr, row_idx, 0)
            grid.addWidget(inp_need, row_idx, 1)
            grid.addWidget(inp_cidr, row_idx, 2)
            grid.addWidget(inp_net, row_idx, 3)
            grid.addWidget(lbl_status, row_idx, 4)
            grid.addWidget(lbl_summary, row_idx, 5)
            grid.addWidget(btn_show, row_idx, 6)

        grid.setColumnStretch(5, 1)
        main_layout.addWidget(table_card)
        main_layout.addStretch()

    def load_preset_1(self):
        self._apply_problem(VlsmSolver.preset_cours_1())

    def load_preset_2(self):
        self._apply_problem(VlsmSolver.preset_cours_2())

    def load_random_problem(self):
        self._apply_problem(VlsmSolver.generate_random_problem())

    def _apply_problem(self, problem: VlsmProblem):
        self.current_problem = problem
        self.used_show_on_current = False
        self.rewarded_current = False
        self.row_shown = [False, False, False]

        self.lbl_base_net.setText(f"{problem.base_network_str}/{problem.base_cidr}")
        needs_str = " , ".join(str(n) for n in problem.unsorted_needs)
        self.lbl_unsorted_needs.setText(needs_str)

        for i in range(3):
            for widget in (self.need_inputs[i], self.cidr_inputs[i], self.net_inputs[i]):
                widget.blockSignals(True)
                widget.clear()
                widget.blockSignals(False)

            self._update_row_visuals(i, is_valid=False)
            self.show_buttons[i].setText("Show")

    def _parse_cidr(self, text: str) -> int:
        cleaned = text.strip().lstrip("/")
        return int(cleaned) if cleaned.isdigit() else -1

    def validate_row(self, row_idx: int):
        if self.current_problem is None:
            return
        alloc = self.current_problem.allocations[row_idx]

        need_txt = self.need_inputs[row_idx].text().strip()
        need_ok = need_txt.isdigit() and int(need_txt) == alloc.hosts_needed

        cidr_val = self._parse_cidr(self.cidr_inputs[row_idx].text())
        cidr_ok = (cidr_val == alloc.cidr)

        net_norm = IPv4MathEngine.normalize_ip_input(self.net_inputs[row_idx].text())
        net_ok = (net_norm == alloc.network_str)

        is_valid = need_ok and cidr_ok and net_ok
        self._update_row_visuals(row_idx, is_valid=is_valid)
        self._check_all_solved()

    def _update_row_visuals(self, row_idx: int, is_valid: bool):
        lbl_status = self.status_labels[row_idx]
        badge = self.summary_badges[row_idx]

        if is_valid and self.current_problem is not None:
            alloc = self.current_problem.allocations[row_idx]
            lbl_status.setText("✓")
            lbl_status.setObjectName("statusCorrect")
            badge.setText(alloc.last_octet_summary)
            badge.setProperty("solved", True)
        else:
            lbl_status.setText("✕")
            lbl_status.setObjectName("statusWrong")
            badge.setText("Validez Besoin + /CIDR + Réseau...")
            badge.setProperty("solved", False)

        lbl_status.style().unpolish(lbl_status)
        lbl_status.style().polish(lbl_status)
        badge.style().unpolish(badge)
        badge.style().polish(badge)

    def toggle_show_row(self, row_idx: int):
        if self.current_problem is None:
            return
        self.used_show_on_current = True
        self.row_shown[row_idx] = not self.row_shown[row_idx]
        alloc = self.current_problem.allocations[row_idx]

        if self.row_shown[row_idx]:
            self.need_inputs[row_idx].setText(str(alloc.hosts_needed))
            self.cidr_inputs[row_idx].setText(f"/{alloc.cidr}")
            self.net_inputs[row_idx].setText(alloc.network_str)
            self.show_buttons[row_idx].setText("Hide")
        else:
            self.need_inputs[row_idx].clear()
            self.cidr_inputs[row_idx].clear()
            self.net_inputs[row_idx].clear()
            self.show_buttons[row_idx].setText("Show")

    def _check_all_solved(self):
        if self.rewarded_current or self.used_show_on_current:
            return
        if all(lbl.text() == "✓" for lbl in self.status_labels):
            self.rewarded_current = True
            if self.on_clean_solve:
                self.on_clean_solve("vlsm_clean")
