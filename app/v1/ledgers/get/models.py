"""Models for Ledgers GET"""

from dataclasses import dataclass


@dataclass
class Ledger:
    """GET model for ledgers"""

    # pylint: disable=invalid-name; API standard
    fundId: str
    glName: str
    glDescription: str
    ledgerId: str
    state: str
    currencyName: str
    currencyDecimal: int
    isHidden: bool
    postDate: str
    # pylint: enable=invalid-name

    def __post_init__(self):
        self.isHidden = bool(self.isHidden)
        self.postDate = None if self.postDate is None else str(self.postDate)
