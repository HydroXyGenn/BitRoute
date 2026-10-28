"""
ui/themes.py
Signature QSS Stylesheets for IPv4 Subnet Toolkit v1.2.0:
- Modern Light Mode (soft slate/blue accents)
- Hacker Console Dark Mode (pure #000000 black & #00FF66 phosphor green)
"""


def get_light_qss() -> str:
    return """
    QMainWindow {
        background-color: #F4F7FB;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }

    QWidget {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
        color: #1E293B;
        font-size: 13px;
    }

    QTabWidget::pane {
        border: 1.5px solid #E2E8F0;
        background: #F8FAFC;
        border-top: none;
        border-bottom-left-radius: 8px;
        border-bottom-right-radius: 8px;
    }

    QTabBar::tab {
        background: #E2E8F0;
        color: #475569;
        font-weight: 600;
        font-size: 13px;
        padding: 8px 14px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        margin-right: 4px;
        border: 1.5px solid #CBD5E1;
        border-bottom: none;
    }

    QTabBar::tab:selected {
        background: #F8FAFC;
        color: #1E40AF;
        border-top: 3px solid #2563EB;
        border-bottom: 1.5px solid #F8FAFC;
    }

    QTabBar::tab:hover:!selected {
        background: #EDF2F7;
        color: #1E293B;
    }

    #btnThemeToggle {
        background-color: #FFFFFF;
        border: 1.5px solid #CBD5E1;
        border-radius: 8px;
        padding: 5px 12px;
        font-weight: 600;
        color: #334155;
        font-size: 12px;
    }

    #btnThemeToggle:hover {
        background-color: #F1F5F9;
        color: #0F172A;
    }

    #streakBadge {
        background-color: #FEF3C7;
        border: 1.5px solid #F59E0B;
        border-radius: 8px;
        padding: 4px 12px;
        font-weight: 700;
        color: #B45309;
        font-size: 12px;
    }

    #headerCard, #mainCard, #tableCard, #inspectorCard, #drawerCard {
        background-color: #FFFFFF;
        border: 1.5px solid #E2E8F0;
        border-radius: 12px;
    }

    #tabTitle {
        font-size: 16px;
        font-weight: 700;
        color: #0F172A;
    }

    #tabSubtitle {
        font-size: 12px;
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
        font-size: 15px;
        font-weight: 700;
        color: #1E293B;
    }

    #bitPosLabel {
        font-size: 11px;
        color: #64748B;
        font-weight: 600;
    }

    QCheckBox#bitCheckBox::indicator {
        width: 20px;
        height: 20px;
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
        font-size: 11px;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
    }

    #syncInput {
        border: 1.5px solid #94A3B8;
        border-radius: 8px;
        padding: 5px 10px;
        font-size: 15px;
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

    #toolBtn, #presetBtn {
        background-color: #F1F5F9;
        border: 1.5px solid #CBD5E1;
        border-radius: 8px;
        color: #334155;
        font-weight: 600;
        padding: 6px 12px;
        font-size: 12px;
    }

    #toolBtn:hover, #presetBtn:hover {
        background-color: #E2E8F0;
        color: #0F172A;
    }

    #choiceBtn {
        background-color: #F8FAFC;
        border: 1.5px solid #CBD5E1;
        border-radius: 7px;
        color: #334155;
        font-weight: 600;
        padding: 4px 11px;
        font-size: 12px;
    }

    #choiceBtn:hover {
        background-color: #EFF6FF;
        border-color: #93C5FD;
    }

    #choiceBtn[selected="true"] {
        background-color: #2563EB;
        border: 1.5px solid #1D4ED8;
        color: #FFFFFF;
    }

    #drillNavBtn {
        background-color: #F1F5F9;
        border: 1.5px solid #CBD5E1;
        border-radius: 8px;
        color: #334155;
        font-weight: 700;
        padding: 7px 16px;
        font-size: 13px;
    }

    #drillNavBtn:hover {
        background-color: #E2E8F0;
    }

    #drillNavBtn[active="true"] {
        background-color: #1D4ED8;
        border: 1.5px solid #1E40AF;
        color: #FFFFFF;
    }

    #topBarContainer {
        background-color: #FFFFFF;
        border: 1.5px solid #DCE6F1;
        border-radius: 12px;
    }

    #targetLabel {
        font-size: 14px;
        font-weight: 700;
        color: #0F172A;
        margin-right: 4px;
    }

    #targetIpDisplay {
        border: 1.5px solid #64748B;
        border-radius: 9px;
        padding: 4px 14px;
        font-size: 14px;
        font-weight: 700;
        color: #0F172A;
        background-color: #FFFFFF;
        font-family: 'Consolas', 'Courier New', monospace;
    }

    #slashLabel {
        font-size: 17px;
        font-weight: 700;
        color: #475569;
    }

    #targetCidrDisplay {
        border: 1.5px solid #64748B;
        border-radius: 8px;
        padding: 4px 12px;
        font-size: 14px;
        font-weight: 700;
        color: #0F172A;
        background-color: #FFFFFF;
        font-family: 'Consolas', 'Courier New', monospace;
    }

    #btnNextProblem {
        background-color: #1D4ED8;
        color: #FFFFFF;
        border: 1.5px solid #1D4ED8;
        border-radius: 8px;
        padding: 6px 16px;
        font-size: 13px;
        font-weight: 700;
    }

    #btnNextProblem:hover {
        background-color: #2563EB;
    }

    #btnNextProblem:pressed {
        background-color: #1E40AF;
    }

    #columnHeader {
        font-size: 13px;
        font-weight: 700;
        color: #1E293B;
        padding-bottom: 2px;
    }

    #rowLabel {
        font-size: 14px;
        font-weight: 700;
        color: #1E293B;
        padding-right: 6px;
    }

    #subnetInput {
        border: 1.5px solid #64748B;
        border-radius: 8px;
        padding: 5px 10px;
        font-size: 14px;
        font-weight: 600;
        color: #0F172A;
        background-color: #FFFFFF;
        font-family: 'Consolas', 'Courier New', monospace;
    }

    #subnetInput:focus {
        border: 2px solid #2563EB;
    }

    #answerField {
        border: 1.5px solid #CBD5E1;
        border-radius: 8px;
        padding: 5px 10px;
        font-size: 13px;
        font-weight: 600;
        color: #334155;
        background-color: #F8FAFC;
        font-family: 'Consolas', 'Courier New', monospace;
    }

    #autoSummaryBadge {
        border: 1.5px solid #CBD5E1;
        border-radius: 8px;
        padding: 5px 10px;
        font-size: 12px;
        font-weight: 600;
        color: #64748B;
        background-color: #F8FAFC;
        font-family: 'Consolas', 'Courier New', monospace;
    }

    #autoSummaryBadge[solved="true"] {
        border: 1.5px solid #22C55E;
        color: #15803D;
        background-color: #F0FDF4;
    }

    #statusWrong {
        font-size: 16px;
        font-weight: 900;
        color: #DC2626;
    }

    #statusCorrect {
        font-size: 16px;
        font-weight: 900;
        color: #16A34A;
    }

    #btnShow {
        background-color: transparent;
        color: #0284C7;
        border: 1.5px solid #BAE6FD;
        border-radius: 8px;
        padding: 4px 12px;
        font-size: 12px;
        font-weight: 600;
    }

    #btnShow:hover {
        background-color: #E0F2FE;
        color: #0369A1;
    }

    #monoDetailLabel {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 12px;
        font-weight: 600;
        color: #1E293B;
    }

    #inspectorValueValid {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 13px;
        font-weight: 700;
        color: #15803D;
    }

    #inspectorValueInvalid {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 13px;
        font-weight: 700;
        color: #DC2626;
    }

    #inspectorValueMono {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 13px;
        font-weight: 700;
        color: #1E40AF;
    }

    #tipBanner {
        background-color: #1E293B;
        border-top: 2px solid #3B82F6;
        padding: 4px 14px;
    }

    #tipBannerLabel {
        color: #F8FAFC;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 12px;
        font-weight: 600;
    }

    #btnNextTip {
        background-color: #334155;
        color: #FACC15;
        border: 1px solid #475569;
        border-radius: 6px;
        padding: 3px 10px;
        font-size: 12px;
        font-weight: 700;
    }

    #btnNextTip:hover {
        background-color: #475569;
    }

    #advancementToast {
        background-color: #1E293B;
        border: 2px solid #FACC15;
        border-radius: 10px;
    }

    #advancementTitle {
        color: #FACC15;
        font-weight: 800;
        font-size: 13px;
    }

    #advancementDesc {
        color: #FFFFFF;
        font-weight: 600;
        font-size: 12px;
    }
    """


def get_dark_qss() -> str:
    return """
    /* ================= HACKER CONSOLE BLACK & GREEN THEME ================= */
    QMainWindow {
        background-color: #000000;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }

    QWidget {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
        color: #00FF66;
        font-size: 13px;
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
        font-weight: 600;
        font-size: 13px;
        padding: 8px 14px;
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
        padding: 5px 12px;
        font-weight: 600;
        color: #00FF66;
        font-size: 12px;
    }

    #btnThemeToggle:hover {
        background-color: #00FF66;
        color: #000000;
    }

    #streakBadge {
        background-color: #001A08;
        border: 1.5px solid #00FF66;
        border-radius: 8px;
        padding: 4px 12px;
        font-weight: 700;
        color: #00FF66;
        font-size: 12px;
    }

    #headerCard, #mainCard, #tableCard, #inspectorCard, #drawerCard {
        background-color: #040A04;
        border: 1.5px solid #00551A;
        border-radius: 12px;
    }

    #tabTitle {
        font-size: 16px;
        font-weight: 700;
        color: #00FF66;
    }

    #tabSubtitle {
        font-size: 12px;
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
        font-size: 15px;
        font-weight: 700;
        color: #00FF66;
    }

    #bitPosLabel {
        font-size: 11px;
        color: #009933;
        font-weight: 600;
    }

    QCheckBox#bitCheckBox::indicator {
        width: 20px;
        height: 20px;
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
        font-size: 11px;
        font-weight: 700;
        color: #00CC55;
        text-transform: uppercase;
    }

    #syncInput {
        border: 1.5px solid #007722;
        border-radius: 8px;
        padding: 5px 10px;
        font-size: 15px;
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
        font-weight: 600;
        color: #00CC55;
        font-size: 13px;
    }

    #toolBtn, #presetBtn {
        background-color: #040A04;
        border: 1.5px solid #007722;
        border-radius: 8px;
        color: #00FF66;
        font-weight: 600;
        padding: 6px 12px;
        font-size: 12px;
    }

    #toolBtn:hover, #presetBtn:hover {
        background-color: #00FF66;
        color: #000000;
    }

    #choiceBtn {
        background-color: #020702;
        border: 1.5px solid #00551A;
        border-radius: 7px;
        color: #00CC55;
        font-weight: 600;
        padding: 4px 11px;
        font-size: 12px;
    }

    #choiceBtn:hover {
        border-color: #00FF66;
        color: #00FF66;
    }

    #choiceBtn[selected="true"] {
        background-color: #00FF66;
        border: 1.5px solid #00FF66;
        color: #000000;
    }

    #drillNavBtn {
        background-color: #040A04;
        border: 1.5px solid #00551A;
        border-radius: 8px;
        color: #00CC55;
        font-weight: 700;
        padding: 7px 16px;
        font-size: 13px;
    }

    #drillNavBtn:hover {
        border-color: #00FF66;
        color: #00FF66;
    }

    #drillNavBtn[active="true"] {
        background-color: #00FF66;
        border: 1.5px solid #00FF66;
        color: #000000;
    }

    #topBarContainer {
        background-color: #040A04;
        border: 1.5px solid #00551A;
        border-radius: 12px;
    }

    #targetLabel {
        font-size: 14px;
        font-weight: 700;
        color: #00FF66;
        margin-right: 4px;
    }

    #targetIpDisplay {
        border: 1.5px solid #00882E;
        border-radius: 9px;
        padding: 4px 14px;
        font-size: 14px;
        font-weight: 700;
        color: #00FF66;
        background-color: #000000;
        font-family: 'Consolas', 'Courier New', monospace;
    }

    #slashLabel {
        font-size: 17px;
        font-weight: 700;
        color: #00AA44;
    }

    #targetCidrDisplay {
        border: 1.5px solid #00882E;
        border-radius: 8px;
        padding: 4px 12px;
        font-size: 14px;
        font-weight: 700;
        color: #00FF66;
        background-color: #000000;
        font-family: 'Consolas', 'Courier New', monospace;
    }

    #btnNextProblem {
        background-color: #00551A;
        color: #00FF66;
        border: 1.5px solid #00FF66;
        border-radius: 8px;
        padding: 6px 16px;
        font-size: 13px;
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
        font-size: 13px;
        font-weight: 700;
        color: #00CC55;
        padding-bottom: 2px;
    }

    #rowLabel {
        font-size: 14px;
        font-weight: 700;
        color: #00FF66;
        padding-right: 6px;
    }

    #subnetInput {
        border: 1.5px solid #007722;
        border-radius: 8px;
        padding: 5px 10px;
        font-size: 14px;
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
        border-radius: 8px;
        padding: 5px 10px;
        font-size: 13px;
        font-weight: 600;
        color: #00AA44;
        background-color: #020702;
        font-family: 'Consolas', 'Courier New', monospace;
    }

    #autoSummaryBadge {
        border: 1.5px solid #004414;
        border-radius: 8px;
        padding: 5px 10px;
        font-size: 12px;
        font-weight: 600;
        color: #007722;
        background-color: #010401;
        font-family: 'Consolas', 'Courier New', monospace;
    }

    #autoSummaryBadge[solved="true"] {
        border: 1.5px solid #00FF66;
        color: #00FF66;
        background-color: #00220A;
    }

    #statusWrong {
        font-size: 16px;
        font-weight: 900;
        color: #FF3344;
    }

    #statusCorrect {
        font-size: 16px;
        font-weight: 900;
        color: #00FF66;
    }

    #btnShow {
        background-color: #020702;
        color: #00FF66;
        border: 1.5px solid #007722;
        border-radius: 8px;
        padding: 4px 12px;
        font-size: 12px;
        font-weight: 600;
    }

    #btnShow:hover {
        background-color: #00FF66;
        color: #000000;
    }

    #monoDetailLabel {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 12px;
        font-weight: 600;
        color: #00FF66;
    }

    #inspectorValueValid {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 13px;
        font-weight: 700;
        color: #00FF66;
    }

    #inspectorValueInvalid {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 13px;
        font-weight: 700;
        color: #FF3344;
    }

    #inspectorValueMono {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 13px;
        font-weight: 700;
        color: #33FF88;
    }

    #tipBanner {
        background-color: #030A03;
        border-top: 2px solid #00FF66;
        padding: 4px 14px;
    }

    #tipBannerLabel {
        color: #00FF66;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 12px;
        font-weight: 600;
    }

    #btnNextTip {
        background-color: #061506;
        color: #00FF66;
        border: 1px solid #00AA44;
        border-radius: 6px;
        padding: 3px 10px;
        font-size: 12px;
        font-weight: 700;
    }

    #btnNextTip:hover {
        background-color: #00FF66;
        color: #000000;
    }

    #advancementToast {
        background-color: #001806;
        border: 2px solid #00FF66;
        border-radius: 10px;
    }

    #advancementTitle {
        color: #00FF66;
        font-weight: 800;
        font-size: 13px;
    }

    #advancementDesc {
        color: #A7F3D0;
        font-weight: 600;
        font-size: 12px;
    }
    """
