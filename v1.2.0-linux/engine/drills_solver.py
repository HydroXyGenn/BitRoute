"""
engine/drills_solver.py
Generators and solvers for Tab 4 Flash Drills:
1. IPv4 MTU Fragmentation (Header Length = IHL*4, Offset in 8-byte units, MF flag)
2. Routing & Longest Prefix Match (LPM, Administrative Distance, Metric, Default Route)
3. IPv4 Header Checksum (16-bit one's complement with end-around carry)
Zero GUI dependencies.
"""

from dataclasses import dataclass
import ipaddress
import random
from typing import List, Tuple


# ============================================================================
# DRILL 1: MTU FRAGMENTATION
# ============================================================================

@dataclass(frozen=True)
class MtuFragment:
    """Single IPv4 fragment specification."""
    index: int             # 1-based fragment number
    total_length: int      # payload + header_length
    payload_bytes: int     # data bytes in this fragment
    offset_units: int      # byte_offset // 8
    mf_flag: int           # 1 if More Fragments follow, 0 for last fragment


@dataclass(frozen=True)
class MtuProblem:
    """Complete IPv4 MTU fragmentation exercise."""
    title: str
    total_length: int
    ihl: int
    mtu: int
    header_length: int
    original_data: int
    max_fragment_data: int
    fragments: List[MtuFragment]


# ============================================================================
# DRILL 2: ROUTING & LONGEST PREFIX MATCH (LPM)
# ============================================================================

@dataclass(frozen=True)
class RouteEntry:
    """Single row in a router's routing table."""
    row_id: int            # 1..4
    protocol_code: str     # "C", "S", "O", "R", "S*"
    network_prefix: str    # e.g. "192.168.1.0/24"
    cidr: int              # e.g. 24
    admin_distance: int    # C=0, S=1, O=110, R=120
    metric: int            # e.g. 0, 1, 10, 20
    next_hop: str          # e.g. "10.0.0.1" or "Directement connecté"
    interface: str         # e.g. "GigabitEthernet0/0"

    @property
    def bracket_str(self) -> str:
        if self.protocol_code == "C":
            return "Direct"
        return f"[{self.admin_distance}/{self.metric}]"


@dataclass(frozen=True)
class LpmProblem:
    """Complete Routing Table & LPM exercise."""
    title: str
    destination_ip: str
    routes: List[RouteEntry]
    winning_row_id: int
    decisive_rule: str     # "Longest Prefix Match", "Distance Administrative (AD)", "Métrique", "Route par défaut"
    explanation: str


# ============================================================================
# DRILL 3: IPV4 HEADER CHECKSUM (16-BIT)
# ============================================================================

@dataclass(frozen=True)
class ChecksumProblem:
    """IPv4 16-bit Header Checksum calculation problem."""
    title: str
    words_hex: List[str]   # e.g. ["4500", "0054", ...]
    raw_sum: int           # e.g. 0x2470E
    carried_sum: int       # e.g. 0x4710
    checksum: int          # e.g. 0xB8EF

    @property
    def raw_sum_hex(self) -> str:
        return f"0x{self.raw_sum:X}"

    @property
    def carried_sum_hex(self) -> str:
        return f"0x{self.carried_sum:04X}"

    @property
    def checksum_hex(self) -> str:
        return f"0x{self.checksum:04X}"


class DrillsSolver:
    """Stateless solver and generator for MTU, LPM Routing, and Header Checksum drills."""

    # ------------------------------------------------------------------------
    # 1. MTU FRAGMENTATION
    # ------------------------------------------------------------------------
    @staticmethod
    def solve_mtu(total_length: int, ihl: int, mtu: int, title: str = "Fragmentation IPv4") -> MtuProblem:
        header_len = ihl * 4
        orig_data = max(0, total_length - header_len)
        max_data = ((mtu - header_len) // 8) * 8
        if max_data <= 0:
            raise ValueError("MTU must allow at least 8 bytes of payload.")

        fragments: List[MtuFragment] = []
        remaining = orig_data
        byte_pos = 0
        idx = 1

        while remaining > 0:
            payload = min(max_data, remaining)
            remaining -= payload
            mf = 1 if remaining > 0 else 0
            offset = byte_pos // 8
            fragments.append(
                MtuFragment(
                    index=idx,
                    total_length=payload + header_len,
                    payload_bytes=payload,
                    offset_units=offset,
                    mf_flag=mf,
                )
            )
            byte_pos += payload
            idx += 1

        return MtuProblem(
            title=title,
            total_length=total_length,
            ihl=ihl,
            mtu=mtu,
            header_length=header_len,
            original_data=orig_data,
            max_fragment_data=max_data,
            fragments=fragments,
        )

    @classmethod
    def preset_mtu_cours(cls) -> MtuProblem:
        """
        Official INPT Course Exercise:
        Total Length = 4000, IHL = 5 (20B header), MTU = 1500
        -> 3 fragments: payloads 1480, 1480, 1020; offsets 0, 185, 370; MF 1, 1, 0.
        """
        return cls.solve_mtu(
            total_length=4000,
            ihl=5,
            mtu=1500,
            title="Ex. Cours (Total = 4000 octets, IHL = 5, MTU = 1500)",
        )

    @classmethod
    def generate_random_mtu(cls) -> MtuProblem:
        """
        Generates a 3-fragment MTU problem with realistic parameters.
        """
        presets: List[Tuple[int, int, int]] = [
            (4000, 5, 1500),   # Course classic: 1480, 1480, 1020
            (3500, 5, 1500),   # 1480, 1480, 520 (offsets 0, 185, 370)
            (2800, 5, 1020),   # max_data = 1000 (div by 8: 125) -> 1000, 1000, 780 (offsets 0, 125, 250)
            (1800, 5, 700),    # max_data = 680 (div by 8: 85) -> 680, 680, 420 (offsets 0, 85, 170)
            (1500, 5, 620),    # max_data = 600 (div by 8: 75) -> 600, 600, 280 (offsets 0, 75, 150)
            (2400, 6, 1008),   # IHL=6 (24B header), MTU=1008 -> max_data=984 (offset step 123) -> 984, 984, 408
        ]
        tot, ihl, mtu = random.choice(presets)
        return cls.solve_mtu(
            total_length=tot,
            ihl=ihl,
            mtu=mtu,
            title=f"Fragmentation (Total = {tot} octets, IHL = {ihl}, MTU = {mtu})",
        )

    # ------------------------------------------------------------------------
    # 2. ROUTING & LONGEST PREFIX MATCH (LPM)
    # ------------------------------------------------------------------------
    @staticmethod
    def ip_matches_prefix(ip_str: str, prefix_str: str) -> bool:
        ip_obj = ipaddress.IPv4Address(ip_str)
        net_obj = ipaddress.IPv4Network(prefix_str, strict=False)
        return ip_obj in net_obj

    @classmethod
    def generate_lpm_problem(cls, scenario: str = "random") -> LpmProblem:
        """
        Generates a 4-route routing decision exercise testing one of the 4 router rules:
        - 'Longest Prefix Match'
        - 'Distance Administrative (AD)'
        - 'Métrique'
        - 'Route par défaut'
        """
        scenarios = ["lpm", "ad", "metric", "default"]
        chosen = scenario if scenario in scenarios else random.choice(scenarios)

        if chosen == "lpm":
            sub_octet = random.randint(10, 99)
            host_octet = random.randint(2, 250)
            dest_ip = f"192.168.{sub_octet}.{host_octet}"
            routes = [
                RouteEntry(1, "O", "192.168.0.0/16", 16, 110, 20, "10.0.0.1", "Gi0/0"),
                RouteEntry(2, "R", f"192.168.{sub_octet}.0/24", 24, 120, 2, "10.0.0.2", "Gi0/1"),
                RouteEntry(3, "S", f"192.168.{sub_octet}.0/26", 26, 1, 0, "10.0.0.3", "Gi0/2")
                if host_octet > 64
                else RouteEntry(3, "O", f"192.168.{sub_octet + 1}.0/24", 24, 110, 10, "10.0.0.3", "Gi0/2"),
                RouteEntry(4, "S*", "0.0.0.0/0", 0, 1, 0, "10.0.0.254", "Serial0/0"),
            ]
            # Wait: if host_octet <= 64, make route 2 (/25 or /24) the most specific matching route
            if host_octet <= 63:
                routes[1] = RouteEntry(2, "R", f"192.168.{sub_octet}.0/25", 25, 120, 3, "10.0.0.2", "Gi0/1")
                routes[2] = RouteEntry(3, "S", f"192.168.{sub_octet}.0/24", 24, 1, 0, "10.0.0.3", "Gi0/2")
                winning_id = 2
                explanation = (
                    f"La route #2 (/25) a un masque plus long que #3 (/24) et #1 (/16). "
                    f"Le Longest Prefix Match l'emporte même si RIP (AD=120) a une AD supérieure à Static (AD=1)."
                )
            else:
                # host_octet > 64: route 3 (192.168.sub.0/26 covers .0-.63) does NOT match!
                winning_id = 2
                explanation = (
                    f"Attention au piège : la route #3 (/26) ne couvre que .0 à .63, donc {dest_ip} "
                    f"n'y appartient pas ! Parmi les routes correspondantes (#1 /16, #2 /24, #4 /0), "
                    f"la route #2 (/24) possède le préfixe le plus long."
                )
            return LpmProblem(
                title="Scénario : Plus Long Préfixe (LPM)",
                destination_ip=dest_ip,
                routes=routes,
                winning_row_id=winning_id,
                decisive_rule="Longest Prefix Match",
                explanation=explanation,
            )

        if chosen == "ad":
            sub_octet = random.randint(10, 50)
            dest_ip = f"172.16.{sub_octet}.{random.randint(10, 200)}"
            routes = [
                RouteEntry(1, "O", "172.16.0.0/16", 16, 110, 10, "10.1.1.1", "Gi0/0"),
                RouteEntry(2, "R", f"172.16.{sub_octet}.0/24", 24, 120, 1, "10.1.1.2", "Gi0/1"),
                RouteEntry(3, "O", f"172.16.{sub_octet}.0/24", 24, 110, 50, "10.1.1.3", "Gi0/2"),
                RouteEntry(4, "S*", "0.0.0.0/0", 0, 1, 0, "10.1.1.254", "Serial0/0"),
            ]
            return LpmProblem(
                title="Scénario : Égalité de Préfixe → Distance Administrative (AD)",
                destination_ip=dest_ip,
                routes=routes,
                winning_row_id=3,
                decisive_rule="Distance Administrative (AD)",
                explanation=(
                    f"Les routes #2 et #3 ont le même préfixe le plus long (/24). "
                    f"On départage par la Distance Administrative : OSPF (AD = 110) bat RIP (AD = 120)."
                ),
            )

        if chosen == "metric":
            sub_octet = random.randint(1, 30)
            dest_ip = f"10.10.{sub_octet}.{random.randint(5, 200)}"
            routes = [
                RouteEntry(1, "O", "10.10.0.0/16", 16, 110, 5, "192.168.1.1", "Gi0/0"),
                RouteEntry(2, "O", f"10.10.{sub_octet}.0/24", 24, 110, 65, "192.168.1.2", "Gi0/1"),
                RouteEntry(3, "O", f"10.10.{sub_octet}.0/24", 24, 110, 20, "192.168.1.3", "Gi0/2"),
                RouteEntry(4, "R", f"10.10.{sub_octet}.0/24", 24, 120, 2, "192.168.1.4", "Gi0/3"),
            ]
            return LpmProblem(
                title="Scénario : Même Préfixe & Même Protocole → Métrique",
                destination_ip=dest_ip,
                routes=routes,
                winning_row_id=3,
                decisive_rule="Métrique",
                explanation=(
                    f"Les routes #2 et #3 ont le même préfixe (/24) et le même protocole OSPF (AD = 110). "
                    f"Le routeur choisit la plus petite métrique : 20 < 65 (Route #3)."
                ),
            )

        # Default route scenario
        dest_ip = f"8.8.{random.randint(1, 200)}.{random.randint(1, 200)}"
        routes = [
            RouteEntry(1, "C", "192.168.1.0/24", 24, 0, 0, "Direct", "Gi0/0"),
            RouteEntry(2, "O", "10.0.0.0/8", 8, 110, 20, "192.168.1.2", "Gi0/1"),
            RouteEntry(3, "S", "172.16.0.0/12", 12, 1, 0, "192.168.1.3", "Gi0/2"),
            RouteEntry(4, "S*", "0.0.0.0/0", 0, 1, 0, "203.0.113.1", "Serial0/0"),
        ]
        return LpmProblem(
            title="Scénario : Passerelle de Dernier Recours (0.0.0.0/0)",
            destination_ip=dest_ip,
            routes=routes,
            winning_row_id=4,
            decisive_rule="Route par défaut",
            explanation=(
                f"Aucune route spécifique (#1, #2, #3) ne correspond à l'adresse publique {dest_ip}. "
                f"Le paquet emprunte la route par défaut 0.0.0.0/0 (Route #4)."
            ),
        )

    # ------------------------------------------------------------------------
    # 3. IPV4 HEADER CHECKSUM (16-BIT)
    # ------------------------------------------------------------------------
    @staticmethod
    def solve_checksum(words_hex: List[str], title: str = "Calcul de Checksum IPv4") -> ChecksumProblem:
        """
        Adds 16-bit hex words, applies end-around carry, and takes 16-bit one's complement.
        """
        cleaned_words = [w.strip().upper().replace("0X", "").zfill(4) for w in words_hex]
        raw_sum = sum(int(w, 16) for w in cleaned_words)

        carried = raw_sum
        while carried > 0xFFFF:
            carried = (carried & 0xFFFF) + (carried >> 16)

        checksum = (~carried) & 0xFFFF
        return ChecksumProblem(
            title=title,
            words_hex=cleaned_words,
            raw_sum=raw_sum,
            carried_sum=carried,
            checksum=checksum,
        )

    @classmethod
    def preset_checksum_cours(cls) -> ChecksumProblem:
        """
        Official INPT Course Example (10 words of 16 bits, checksum field set to 0000):
        4500 0054 0000 4000 4001 0000 C0A8 0068 C0A8 0001
        -> Raw sum = 0x2470E
        -> Carried sum = 0x470E + 0x2 = 0x4710
        -> One's complement = 0xB8EF
        """
        words = [
            "4500", "0054", "0000", "4000", "4001",
            "0000", "C0A8", "0068", "C0A8", "0001",
        ]
        return cls.solve_checksum(
            words_hex=words,
            title="Ex. Cours Complet (10 mots : 4500 0054 ... C0A8 0001)",
        )

    @classmethod
    def generate_short_checksum(cls) -> ChecksumProblem:
        """
        Generates a fast 4-word 16-bit hex checksum exercise so students can
        practice end-around carry and one's complement quickly without calculator fatigue.
        Guarantees at least 1 carry overflow (raw_sum > 0xFFFF).
        """
        while True:
            words = [
                random.choice(["4500", "4510", "4520"]),
                f"{random.randint(0x0028, 0x05DC):04X}",
                f"{random.randint(0x4000, 0x8011):04X}",
                f"{random.randint(0x8000, 0xC0A8):04X}",
            ]
            prob = cls.solve_checksum(
                words_hex=words,
                title="Mode Express (4 mots de 16 bits avec retenue)",
            )
            if prob.raw_sum > 0xFFFF:
                return prob

    @staticmethod
    def parse_hex_input(text: str) -> int:
        """Parses a user hex string (with or without 0x prefix), returning -1 on error."""
        cleaned = text.strip().upper().replace(" ", "")
        if cleaned.startswith("0X"):
            cleaned = cleaned[2:]
        if not cleaned:
            return -1
        try:
            return int(cleaned, 16)
        except ValueError:
            return -1
