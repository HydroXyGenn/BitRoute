"""
engine/vlsm_solver.py
VLSM (Variable Length Subnet Mask) solver and problem generator
including official INPT course presets.
Zero GUI dependencies.
"""

from dataclasses import dataclass
import ipaddress
import math
import random
from typing import List


@dataclass(frozen=True)
class VlsmAllocation:
    """Represents one allocated VLSM subnet row."""
    rank: int                  # 1-based index after sorting descending
    hosts_needed: int          # N machines requested
    host_bits: int             # h such that 2^h - 2 >= N
    cidr: int                  # 32 - h
    block_size: int            # 2^h
    usable_capacity: int       # 2^h - 2
    mask_str: str              # e.g. "255.255.255.128"
    network_str: str           # e.g. "193.225.34.0"
    first_host_str: str        # e.g. "193.225.34.1"
    last_host_str: str         # e.g. "193.225.34.126"
    broadcast_str: str         # e.g. "193.225.34.127"

    @property
    def last_octet_summary(self) -> str:
        """Compact summary displayed auto-magically once CIDR and Network IP are solved."""
        fh_last = self.first_host_str.split(".")[-1]
        lh_last = self.last_host_str.split(".")[-1]
        bc_last = self.broadcast_str.split(".")[-1]
        mk_last = self.mask_str.split(".")[-1]
        return f"Plage: .{fh_last} → .{lh_last}  |  Bcast: .{bc_last}  |  Masque: .{mk_last}"


@dataclass(frozen=True)
class VlsmProblem:
    """Represents a complete VLSM exercise (base network + unsorted needs + sorted solution)."""
    title: str
    base_network_str: str      # e.g. "193.225.34.0"
    base_cidr: int             # e.g. 24
    unsorted_needs: List[int]  # e.g. [44, 20, 100]
    allocations: List[VlsmAllocation]


class VlsmSolver:
    """Implements VLSM subnetting algorithm and official course exercises."""

    @staticmethod
    def smallest_host_bits(hosts_needed: int) -> int:
        """Finds smallest power h >= 2 such that 2^h - 2 >= hosts_needed."""
        if hosts_needed < 1:
            return 2
        h = max(2, math.ceil(math.log2(hosts_needed + 2)))
        while (1 << h) - 2 < hosts_needed:
            h += 1
        return h

    @classmethod
    def solve(
        cls,
        base_network_str: str,
        base_cidr: int,
        needs: List[int],
        title: str = "Exercice VLSM",
    ) -> VlsmProblem:
        """
        Sorts host requirements in strictly descending order and allocates
        subnets sequentially starting from base_network_str.
        """
        base_net = ipaddress.IPv4Network(f"{base_network_str}/{base_cidr}", strict=False)
        current_ip_int = int(base_net.network_address)

        sorted_needs = sorted(needs, reverse=True)
        allocations: List[VlsmAllocation] = []

        for idx, need in enumerate(sorted_needs, start=1):
            h = cls.smallest_host_bits(need)
            cidr = 32 - h
            block_size = 1 << h
            usable = block_size - 2

            subnet = ipaddress.IPv4Network((current_ip_int, cidr), strict=False)
            net_addr = subnet.network_address
            bcast_addr = subnet.broadcast_address
            first_host = net_addr + 1
            last_host = bcast_addr - 1

            allocations.append(
                VlsmAllocation(
                    rank=idx,
                    hosts_needed=need,
                    host_bits=h,
                    cidr=cidr,
                    block_size=block_size,
                    usable_capacity=usable,
                    mask_str=str(subnet.netmask),
                    network_str=str(net_addr),
                    first_host_str=str(first_host),
                    last_host_str=str(last_host),
                    broadcast_str=str(bcast_addr),
                )
            )
            current_ip_int += block_size

        return VlsmProblem(
            title=title,
            base_network_str=str(base_net.network_address),
            base_cidr=base_cidr,
            unsorted_needs=list(needs),
            allocations=allocations,
        )

    @classmethod
    def preset_cours_1(cls) -> VlsmProblem:
        """
        Official INPT Course Exercise 1:
        Base network 193.225.34.0/24 with host needs [44, 20, 100].
        Sorted:
        - 100 hosts -> /25 (255.255.255.128), 193.225.34.0 .. .127
        - 44 hosts  -> /26 (255.255.255.192), 193.225.34.128 .. .191
        - 20 hosts  -> /27 (255.255.255.224), 193.225.34.192 .. .223
        """
        return cls.solve(
            base_network_str="193.225.34.0",
            base_cidr=24,
            needs=[44, 20, 100],
            title="Ex. Cours 1 (193.225.34.0/24 — 44, 20, 100)",
        )

    @classmethod
    def preset_cours_2(cls) -> VlsmProblem:
        """
        Official INPT Course Exercise 2:
        Base network 192.168.0.0/24 with host needs [100, 28, 4].
        Sorted:
        - 100 hosts -> /25, 192.168.0.0/25 (.1 to .126, bcast .127)
        - 28 hosts  -> /27, 192.168.0.128/27 (.129 to .158, bcast .159)
        - 4 hosts   -> /29, 192.168.0.160/29 (.161 to .166, bcast .167)
        """
        return cls.solve(
            base_network_str="192.168.0.0",
            base_cidr=24,
            needs=[28, 4, 100],
            title="Ex. Cours 2 (192.168.0.0/24 — 28, 4, 100)",
        )

    @classmethod
    def generate_random_problem(cls) -> VlsmProblem:
        """
        Generates a random /24 network and 3 distinct host requirements
        whose total VLSM block sizes fit within 256 addresses.
        Presented in shuffled order so the user must apply the descending rule.
        """
        base_choices = [
            f"192.168.{random.randint(1, 250)}.0",
            f"172.{random.randint(16, 31)}.{random.randint(1, 200)}.0",
            f"10.{random.randint(1, 200)}.{random.randint(1, 200)}.0",
        ]
        base_ip = random.choice(base_choices)

        # Pick 3 distinct block exponents h1 > h2 > h3 such that 2^h1 + 2^h2 + 2^h3 <= 256
        valid_triplets = [
            (7, 6, 5),  # 128 + 64 + 32 = 224
            (7, 6, 4),  # 128 + 64 + 16 = 208
            (7, 6, 3),  # 128 + 64 + 8  = 200
            (7, 5, 4),  # 128 + 32 + 16 = 176
            (7, 5, 3),  # 128 + 32 + 8  = 168
            (6, 5, 4),  # 64  + 32 + 16 = 112
            (6, 5, 3),  # 64  + 32 + 8  = 104
        ]
        h1, h2, h3 = random.choice(valid_triplets)

        def random_need_for_h(h: int) -> int:
            low = (1 << (h - 1)) - 1
            high = (1 << h) - 2
            return random.randint(max(2, low), high)

        needs = [random_need_for_h(h1), random_need_for_h(h2), random_need_for_h(h3)]
        # Shuffle so it's not already sorted descending
        random.shuffle(needs)
        if needs == sorted(needs, reverse=True):
            needs[0], needs[1] = needs[1], needs[0]

        return cls.solve(
            base_network_str=base_ip,
            base_cidr=24,
            needs=needs,
            title=f"VLSM Aléatoire ({base_ip}/24)",
        )
