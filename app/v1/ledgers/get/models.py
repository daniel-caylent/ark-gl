"""Models for Ledgers GET"""
from datetime import datetime

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
    postDate: datetime
    # pylint: enable=invalid-name

    def __post_init__(self):
        self.postDate = None if self.postDate is None else self.postDate.strftime("%Y-%m-%dT%H:%M:%SZ")
