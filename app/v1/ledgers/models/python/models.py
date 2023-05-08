from dataclasses import dataclass
from typing import Literal

from shared import validate_uuid    # pylint: disable=import-error

@dataclass
class Ledger:
    fundId: str
    glName: str
    glDescription: str
    ledgerId: str
    state: Literal["USED", "UNUSED", "ACTIVE"]
    currencyName: str
    currencyDecimal: int
    isHidden: bool

    def __post_init__(self):
        self.isHidden = bool(self.isHidden)


@dataclass
class LedgerPost:
    fundId: str
    glName: str
    glDescription: str
    currencyName: str
    currencyDecimal: int
    isHidden: bool = False

    def __post_init__(self):
        self.glName = self.glName.strip()
        self.glDescription = self.glDescription.strip()
        self.currencyName = self.currencyName.strip()
        self.isHidden = bool(self.isHidden)
        self.fundId = validate_uuid(self.fundId, throw=True)
        self.currencyDecimal = int(self.currencyDecimal)


@dataclass
class LedgerPut:
    fundId: str = None
    glName: str = None
    glDescription: str = None
    currencyName: str = None
    currencyDecimal: int = None
    isHidden: bool = False

    def __post_init__(self):
        self.glName = None if self.glName is None else self.glName.strip()
        self.glDescription = (
            None if self.glDescription is None else self.glDescription.strip()
        )
        self.currencyName = (
            None if self.currencyName is None else self.currencyName.strip()
        )
        self.isHidden = None if self.isHidden is None else bool(self.isHidden)
        self.fundId = (
            None if self.fundId is None else validate_uuid(self.fundId, throw=True)
        )
        self.currencyDecimal = (
            None if self.currencyDecimal is None else int(self.currencyDecimal)
        )
