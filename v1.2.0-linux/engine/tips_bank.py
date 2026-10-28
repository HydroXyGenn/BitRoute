"""
engine/tips_bank.py
Minecraft-style rotating tips bank (covering app keyboard shortcuts and INPT
networking course formulas) + Streak & Advancement manager.
Zero GUI dependencies.
"""

from dataclasses import dataclass
import random
from typing import Dict, List, Optional, Set


@dataclass(frozen=True)
class TipEntry:
    """Single tip displayed in the MinecraftTipBanner."""
    category: str   # "[APP TIP]", "[COURS INPT]", "[ASTUCE PRO]"
    text: str

    @property
    def formatted(self) -> str:
        return f"{self.category}  {self.text}"


@dataclass(frozen=True)
class Advancement:
    """Advancement unlocked upon solving exercises without Show."""
    key: str
    title: str
    description: str


TIPS_LIST: List[TipEntry] = [
    TipEntry(
        "[APP TIP]",
        "Dans les champs IP, tapez Espace ou Virgule pour insérer un point '.' instantanément !",
    ),
    TipEntry(
        "[APP TIP]",
        "Smart Auto-Dot v1.2 : dès que vous tapez 2 chiffres ≥ 26 (ex: 32, 99, 68), le point '.' s'ajoute tout seul !",
    ),
    TipEntry(
        "[COURS INPT]",
        "Les 9 seules valeurs valides d'un octet de masque sont : 255, 254, 252, 248, 240, 224, 192, 128 et 0 (bits à 1 contigus).",
    ),
    TipEntry(
        "[COURS INPT]",
        "Règle d'Or VLSM : triez TOUJOURS les besoins en machines du plus grand au plus petit avant de découper !",
    ),
    TipEntry(
        "[ASTUCE PRO]",
        "Magic Number (Pas du sous-réseau) = 256 − Octet du masque. Ex: masque 255.255.255.192 → saut de 256 − 192 = 64.",
    ),
    TipEntry(
        "[COURS INPT]",
        "En VLSM, n'oubliez jamais le +2 : pour N machines, il faut 2^h − 2 ≥ N (1 adresse Réseau + 1 adresse Broadcast).",
    ),
    TipEntry(
        "[COURS INPT]",
        "Fragmentation IPv4 : la charge utile (sauf dernier fragment) DOIT être un multiple de 8 octets ! Offset = Octet_Début / 8.",
    ),
    TipEntry(
        "[COURS INPT]",
        "Longueur de l'en-tête IPv4 = IHL × 4 octets. Avec IHL = 5 (standard sans options), l'en-tête mesure 20 octets.",
    ),
    TipEntry(
        "[COURS INPT]",
        "Priorité du routeur : 1) Préfixe le plus long (LPM) → 2) Distance Administrative (AD) la plus basse → 3) Métrique la plus faible.",
    ),
    TipEntry(
        "[COURS INPT]",
        "Distances Administratives (AD) par défaut : Connecté = 0 | Statique = 1 | OSPF = 110 | RIP = 120.",
    ),
    TipEntry(
        "[COURS INPT]",
        "Plages Privées RFC 1918 : 10.0.0.0/8 (Classe A), 172.16.0.0 à 172.31.255.255 (/12, Classe B), 192.168.0.0/16 (Classe C).",
    ),
    TipEntry(
        "[COURS INPT]",
        "APIPA (169.254.0.0/16) est auto-attribuée quand aucun serveur DHCP ne répond. Loopback = 127.0.0.0/8.",
    ),
    TipEntry(
        "[COURS INPT]",
        "Classes IPv4 (1er octet) : A [0..127] (0...), B [128..191] (10...), C [192..223] (110...), D [224..239] Multicast, E [240..255] Réservé.",
    ),
    TipEntry(
        "[ASTUCE PRO]",
        "Host ID Interne = IP ET (~Masque). L'adresse réseau s'obtient par IP ET Masque.",
    ),
    TipEntry(
        "[COURS INPT]",
        "Checksum IPv4 (16 bits) : additionnez les mots de 16 bits, rabattez la retenue (end-around carry) à droite, puis inversez les bits (~Somme).",
    ),
    TipEntry(
        "[APP TIP]",
        "Validez un exercice complet sans cliquer sur 'Show' pour augmenter votre Série et débloquer des succès !",
    ),
]


ADVANCEMENTS_CATALOG: Dict[str, Advancement] = {
    "subnet_clean": Advancement(
        key="subnet_clean",
        title="Maître du Masque",
        description="Sous-réseau résolu sans utiliser 'Show' !",
    ),
    "vlsm_clean": Advancement(
        key="vlsm_clean",
        title="Architecte VLSM",
        description="Découpage VLSM sans gaspillage d'adresses !",
    ),
    "mtu_clean": Advancement(
        key="mtu_clean",
        title="Chirurgien MTU",
        description="Fragmentation IPv4 découpée au multiple de 8 près !",
    ),
    "lpm_clean": Advancement(
        key="lpm_clean",
        title="Routeur Humain",
        description="Table de routage et règle LPM/AD maîtrisées !",
    ),
    "checksum_clean": Advancement(
        key="checksum_clean",
        title="Seigneur du Checksum",
        description="Somme hexa 16 bits et complément à un parfaits !",
    ),
    "streak_3": Advancement(
        key="streak_3",
        title="Série de 3 (On Fire)",
        description="3 exercices consécutifs validés sans aide !",
    ),
    "streak_5": Advancement(
        key="streak_5",
        title="Ingénieur Réseau INPT",
        description="5 exercices consécutifs validés sans aide !",
    ),
}


class TipsAndStreakManager:
    """Manages rotating tips, streak counter, and unlocked advancements."""

    def __init__(self) -> None:
        self.tips: List[TipEntry] = list(TIPS_LIST)
        self._tip_index: int = 0
        self.streak: int = 0
        self.unlocked_keys: Set[str] = set()

    def next_tip(self, randomize: bool = False) -> TipEntry:
        if randomize:
            self._tip_index = random.randrange(len(self.tips))
        else:
            self._tip_index = (self._tip_index + 1) % len(self.tips)
        return self.tips[self._tip_index]

    def current_tip(self) -> TipEntry:
        return self.tips[self._tip_index]

    def record_clean_solve(self, category_key: str) -> Optional[Advancement]:
        """
        Increments the streak when an exercise is solved without clicking 'Show',
        and returns an Advancement to toast (either newly unlocked or milestone).
        """
        self.streak += 1

        # Check streak milestones first
        if self.streak == 5 and "streak_5" not in self.unlocked_keys:
            self.unlocked_keys.add("streak_5")
            return ADVANCEMENTS_CATALOG["streak_5"]
        if self.streak == 3 and "streak_3" not in self.unlocked_keys:
            self.unlocked_keys.add("streak_3")
            return ADVANCEMENTS_CATALOG["streak_3"]

        adv = ADVANCEMENTS_CATALOG.get(category_key)
        if adv is not None:
            self.unlocked_keys.add(category_key)
            return adv
        return None

    def reset_streak(self) -> None:
        self.streak = 0
