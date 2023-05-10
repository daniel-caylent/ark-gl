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
    currencyName: str
    currencyDecimal: int
    glDescription: str = None
    isHidden: bool = False

    def __post_init__(self):
        self.glName = validate_str(self.glName, 'glName')
        self.fundId = check_uuid(self.fundId, 'fundId')
        self.currencyDecimal = validate_int(self.currencyDecimal, 'currencyDecimal')
        self.currencyName = validate_str(self.currencyName, 'currencyName')
        self.isHidden = bool(self.isHidden)
        self.glDescription = (
            None if self.glDescription is None else self.glDescription.strip()
        )


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


def check_uuid(uuid, name) -> str:
    if uuid is None:
        raise Exception(f'Required argument is missing: {name}.')

    try:
        validate_uuid(uuid, throw=True)
    except:
        raise Exception(f'{name} is not a valid UUID.')

    return uuid

def validate_str(str_, name) -> str:
    if str_ is None:
        raise Exception(f'Required argument is missing: {name}.')

    try:
        str_ = str_.strip()
    except:
        raise Exception(f'{name} is invalid.')

    return str_

def validate_int(int_, name) -> int:
    if int_ is None:
        raise Exception(f'Required argument is missing: {name}.')

    try:
        int_ = int(str(int_))
    except:
        raise Exception(f'{name} is invalid.')
