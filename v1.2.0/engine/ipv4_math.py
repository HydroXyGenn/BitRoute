"""
engine/ipv4_math.py
Pure IPv4 mathematical calculations, octet mask inspection, classful/RFC1918
classification, and 32-bit binary breakdown.
Zero GUI dependencies.
"""

from dataclasses import dataclass
import ipaddress
import random
from typing import Dict, Optional, Tuple


VALID_MASK_OCTETS: Tuple[int, ...] = (255, 254, 252, 248, 240, 224, 192, 128, 0)


@dataclass(frozen=True)
class OctetAnalysis:
    """Result of inspecting a single 8-bit octet (0..255)."""
    value: int
    binary_str: str
    hex_str: str
    is_valid_mask_octet: bool
    ones_complement: int
    ones_complement_binary: str
    block_size: int


@dataclass(frozen=True)
class SubnetAnalysis:
    """Complete analysis of an IPv4 address + CIDR prefix."""
    ip_str: str
    cidr: int
    mask_str: str
    wildcard_str: str
    network_str: str
    broadcast_str: str
    first_host_str: str
    last_host_str: str
    next_subnet_str: str
    internal_host_id_str: str
    ip_class: str
    default_class_cidr: Optional[int]
    leading_bits_pattern: str
    address_type: str  # "Publique", "Privée", "APIPA", "Loopback", "Multicast", "Réservée"
    borrowed_bits: int
    host_bits: int
    num_subnets_from_class: int
    usable_hosts: int
    # 32-bit formatted strings (dotted 8-bit groups)
    ip_bin_dotted: str
    mask_bin_dotted: str
    wildcard_bin_dotted: str
    network_bin_dotted: str
    host_id_bin_dotted: str
    broadcast_bin_dotted: str


class IPv4MathEngine:
    """Stateless utility and OOP facade for IPv4 calculations."""

    @staticmethod
    def is_valid_mask_octet(val: int) -> bool:
        """True if the octet has contiguous 1s from MSB to LSB."""
        return val in VALID_MASK_OCTETS

    @staticmethod
    def ones_complement_octet(val: int) -> int:
        """Returns 8-bit one's complement (~val & 0xFF), i.e., 255 - val."""
        return (~val) & 0xFF

    @staticmethod
    def block_size_octet(val: int) -> int:
        """Returns the subnet step / Magic Number (256 - val)."""
        return 256 - max(0, min(255, val))

    @classmethod
    def analyze_octet(cls, val: int) -> OctetAnalysis:
        """Returns a complete OctetAnalysis for Tab 1 (8-Bit Converter + Mask Inspector)."""
        clamped = max(0, min(255, val))
        comp = cls.ones_complement_octet(clamped)
        return OctetAnalysis(
            value=clamped,
            binary_str=f"{clamped:08b}",
            hex_str=f"0x{clamped:02X}",
            is_valid_mask_octet=cls.is_valid_mask_octet(clamped),
            ones_complement=comp,
            ones_complement_binary=f"{comp:08b}",
            block_size=cls.block_size_octet(clamped),
        )

    @staticmethod
    def classify_ipv4(ip_str: str) -> Tuple[str, Optional[int], str]:
        """
        Determines IPv4 Class (A, B, C, D, E), its default classful CIDR,
        and leading high-order bits pattern according to INPT course rules.
        """
        first_octet = int(ip_str.split(".")[0])
        if 0 <= first_octet <= 127:
            return ("A", 8, "0...")
        if 128 <= first_octet <= 191:
            return ("B", 16, "10...")
        if 192 <= first_octet <= 223:
            return ("C", 24, "110...")
        if 224 <= first_octet <= 239:
            return ("D", None, "1110...")
        return ("E", None, "11110...")

    @staticmethod
    def get_address_type(ip_str: str) -> str:
        """
        Determines address scope/type according to course rules:
        - 'Loopback' : 127.0.0.0/8
        - 'APIPA'    : 169.254.0.0/16
        - 'Privée'   : 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
        - 'Publique' : All other unicast addresses in Classes A, B, C
        """
        parts = [int(p) for p in ip_str.split(".")]
        o1, o2 = parts[0], parts[1]

        if o1 == 127:
            return "Loopback"
        if o1 == 169 and o2 == 254:
            return "APIPA"
        if o1 == 10:
            return "Privée"
        if o1 == 172 and 16 <= o2 <= 31:
            return "Privée"
        if o1 == 192 and o2 == 168:
            return "Privée"
        if 224 <= o1 <= 239:
            return "Multicast"
        if o1 >= 240 or o1 == 0:
            return "Réservée"
        return "Publique"

    @staticmethod
    def int_to_dotted_bin(val_32: int) -> str:
        """Formats a 32-bit integer as 'XXXXXXXX.XXXXXXXX.XXXXXXXX.XXXXXXXX'."""
        b = f"{val_32 & 0xFFFFFFFF:032b}"
        return f"{b[0:8]}.{b[8:16]}.{b[16:24]}.{b[24:32]}"

    @staticmethod
    def int_to_ip_str(val_32: int) -> str:
        """Converts a 32-bit unsigned integer to dotted-decimal IPv4 string."""
        return str(ipaddress.IPv4Address(val_32 & 0xFFFFFFFF))

    @classmethod
    def analyze_subnet(cls, ip_str: str, cidr: int) -> SubnetAnalysis:
        """
        Performs full IPv4 subnetting & binary analysis:
        - Network Address = IP AND Mask
        - Internal Host ID = IP AND (~Mask & 0xFFFFFFFF)
        - Broadcast Address = Network OR (~Mask & 0xFFFFFFFF)
        - First Host, Last Host, Next Subnet
        - Borrowed bits (b_S) and Host bits (b_H)
        """
        cidr = max(1, min(32, int(cidr)))
        ip_obj = ipaddress.IPv4Address(ip_str.strip())
        ip_int = int(ip_obj)

        mask_int = ((0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF) if cidr > 0 else 0
        wildcard_int = (~mask_int) & 0xFFFFFFFF

        network_int = ip_int & mask_int
        host_id_int = ip_int & wildcard_int
        broadcast_int = network_int | wildcard_int

        num_addresses = 1 << (32 - cidr)
        first_host_int = network_int + 1 if cidr <= 30 else network_int
        last_host_int = broadcast_int - 1 if cidr <= 30 else broadcast_int
        next_subnet_int = (network_int + num_addresses) & 0xFFFFFFFF

        ip_class, default_cidr, leading_bits = cls.classify_ipv4(str(ip_obj))
        addr_type = cls.get_address_type(str(ip_obj))

        if default_cidr is not None and cidr >= default_cidr:
            borrowed_bits = cidr - default_cidr
            num_subnets = 1 << borrowed_bits
        else:
            borrowed_bits = 0
            num_subnets = 1

        host_bits = 32 - cidr
        usable_hosts = max(0, (1 << host_bits) - 2)

        return SubnetAnalysis(
            ip_str=str(ip_obj),
            cidr=cidr,
            mask_str=cls.int_to_ip_str(mask_int),
            wildcard_str=cls.int_to_ip_str(wildcard_int),
            network_str=cls.int_to_ip_str(network_int),
            broadcast_str=cls.int_to_ip_str(broadcast_int),
            first_host_str=cls.int_to_ip_str(first_host_int),
            last_host_str=cls.int_to_ip_str(last_host_int),
            next_subnet_str=cls.int_to_ip_str(next_subnet_int),
            internal_host_id_str=cls.int_to_ip_str(host_id_int),
            ip_class=ip_class,
            default_class_cidr=default_cidr,
            leading_bits_pattern=leading_bits,
            address_type=addr_type,
            borrowed_bits=borrowed_bits,
            host_bits=host_bits,
            num_subnets_from_class=num_subnets,
            usable_hosts=usable_hosts,
            ip_bin_dotted=cls.int_to_dotted_bin(ip_int),
            mask_bin_dotted=cls.int_to_dotted_bin(mask_int),
            wildcard_bin_dotted=cls.int_to_dotted_bin(wildcard_int),
            network_bin_dotted=cls.int_to_dotted_bin(network_int),
            host_id_bin_dotted=cls.int_to_dotted_bin(host_id_int),
            broadcast_bin_dotted=cls.int_to_dotted_bin(broadcast_int),
        )

    @classmethod
    def generate_practice_problem(cls) -> SubnetAnalysis:
        """
        Generates a balanced random IPv4 problem for Tab 2 so the student
        encounters Public, Private (A/B/C), APIPA, and Loopback addresses,
        with CIDR >= default classful prefix (up to /30).
        """
        roll = random.random()
        if roll < 0.12:
            # Loopback 127.x.x.x (Class A)
            o1 = 127
            o2 = random.randint(0, 255)
            o3 = random.randint(0, 255)
            o4 = random.randint(1, 254)
            cidr = random.randint(8, 30)
        elif roll < 0.24:
            # APIPA 169.254.x.x (Class B)
            o1 = 169
            o2 = 254
            o3 = random.randint(0, 255)
            o4 = random.randint(1, 254)
            cidr = random.randint(16, 30)
        elif roll < 0.58:
            # Private RFC 1918 (Class A, B, or C)
            priv_choice = random.choice(["A", "B", "C"])
            if priv_choice == "A":
                o1 = 10
                o2 = random.randint(0, 255)
                o3 = random.randint(0, 255)
                cidr = random.randint(8, 30)
            elif priv_choice == "B":
                o1 = 172
                o2 = random.randint(16, 31)
                o3 = random.randint(0, 255)
                cidr = random.randint(16, 30)
            else:
                o1 = 192
                o2 = 168
                o3 = random.randint(0, 255)
                cidr = random.randint(24, 30)
            o4 = random.randint(1, 254)
        else:
            # Public Unicast (Class A, B, or C)
            pub_class = random.choice(["A", "B", "C"])
            if pub_class == "A":
                o1 = random.choice([i for i in range(1, 127) if i != 10])
                o2 = random.randint(0, 255)
                cidr = random.randint(8, 30)
            elif pub_class == "B":
                o1 = random.randint(128, 191)
                o2 = random.randint(0, 255)
                if o1 == 172 and 16 <= o2 <= 31:
                    o2 = 32
                if o1 == 169 and o2 == 254:
                    o2 = 253
                cidr = random.randint(16, 30)
            else:
                o1 = random.randint(192, 223)
                o2 = random.randint(0, 255)
                if o1 == 192 and o2 == 168:
                    o2 = 169
                cidr = random.randint(24, 30)
            o3 = random.randint(0, 255)
            o4 = random.randint(1, 254)

        ip_str = f"{o1}.{o2}.{o3}.{o4}"
        return cls.analyze_subnet(ip_str, cidr)

    @staticmethod
    def normalize_ip_input(raw_text: str) -> str:
        """Normalizes user IP input (spaces, commas, dots) into standard 'a.b.c.d'."""
        cleaned_parts = []
        cur_oct = ""
        for ch in raw_text.strip():
            if ch.isdigit():
                cur_oct += ch
            else:
                if cur_oct:
                    cleaned_parts.append(str(int(cur_oct)))
                    cur_oct = ""
        if cur_oct:
            cleaned_parts.append(str(int(cur_oct)))
        return ".".join(cleaned_parts)
