"""Models for Ledgers GET"""

from dataclasses import dataclass


@dataclass
class Ledger:
    fundId: str
    glName: str
    glDescription: str
    ledgerId: str
    state: str
    currencyName: str
    currencyDecimal: int
    isHidden: bool

    def __post_init__(self):
        self.isHidden = bool(self.isHidden)
