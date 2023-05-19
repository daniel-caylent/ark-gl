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
        self.fundId = check_uuid(self.fundId, 'fundId')
        self.glName = validate_str(self.glName, 'glName', min_len=3, max_len=128)
        self.currencyDecimal = validate_int(self.currencyDecimal, 'currencyDecimal', allowed=[0,2,3,4])
        self.currencyName = validate_str(self.currencyName, 'currencyName', min_len=3, max_len=3)
        self.isHidden = bool(self.isHidden)
        self.glDescription = (
            None if self.glDescription is None else
            validate_str(self.glDescription, 'glDescription', min_len=3, max_len=256)
        )


@dataclass
class LedgerPut:
    glName: str = None
    glDescription: str = None
    currencyName: str = None
    currencyDecimal: int = None
    isHidden: bool = False

    def __post_init__(self):
        self.glName = None if self.glName is None else validate_str(self.glName, 'glName', min_len=3, max_len=128)
        self.currencyDecimal = (
            None if self.currencyDecimal is None else
            validate_int(self.currencyDecimal, 'currencyDecimal', allowed=[0,2,3,4])
        )
        self.currencyName = (
            None if self.currencyName is None else
            validate_str(self.currencyName, 'currencyName', min_len=3, max_len=3)
        )
        self.glDescription = (
            None if self.glDescription is None else
            validate_str(self.glDescription, 'glDescription', min_len=3, max_len=256)
        )
        self.isHidden = None if self.isHidden is None else bool(self.isHidden)


def check_uuid(uuid, name) -> str:
    if uuid is None:
        raise Exception(f'Required argument is missing: {name}.')

    try:
        validate_uuid(uuid, throw=True)
    except:
        raise Exception(f'{name} is not a valid UUID.')

    return uuid

def validate_str(str_, name, min_len=0, max_len=255) -> str:
    if str_ is None:
        raise Exception(f'Required argument is missing: {name}.')

    try:
        str_ = str_.strip()
    except:
        raise Exception(f'{name} is invalid.')
    
    if len(str_) < min_len:
        raise Exception(f'{name} does not meet min length required of {min_len} characters.')
    if len(str_) > max_len:
        raise Exception(f'{name} does not meet max length required of {max_len} characters.')

    return str_

def validate_int(int_, name, allowed: list=None) -> int:
    if int_ is None:
        raise Exception(f'Required argument is missing: {name}.')

    try:
        int_ = int(str(int_))
    except:
        raise Exception(f'{name} is invalid.')

    if allowed:
        if int_ not in allowed:
            raise Exception(f'{name} must be one of {allowed}.')

    return int_