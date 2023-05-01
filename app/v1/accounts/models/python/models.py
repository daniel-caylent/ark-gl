from dataclasses import dataclass
from typing import Literal

from shared import validate_uuid    # pylint: disable=import-error

@dataclass
class Account:
    accountNo: str
    accountName: str
    state: Literal["USED", "UNUSED", "ACTIVE"]
    accountDescription: str
    fsMappingId: str
    fsName: str
    isHidden: bool
    isTaxable: bool
    isEntityRequired: bool
    parentAccountId: str
    attributeId: str
    accountId: str
    fundId: str

    def __post_init__(self):
        self.isEntityRequired = bool(self.isEntityRequired)
        self.isHidden = bool(self.isHidden)
        self.isTaxable = bool(self.isTaxable)


@dataclass
class AccountPost:
    accountNo: str
    accountName: str
    accountDescription: str
    fsMappingId: str
    fsName: str
    attributeId: str
    fundId: str
    isEntityRequired: bool
    isTaxable: bool
    isDryRun: bool = False
    parentAccountId: str = None
    isHidden: bool = False
    state: Literal["USED", "UNUSED", "ACTIVE"] = "UNUSED"

    def __post_init__(self):
        self.accountNo = str(int(self.accountNo))
        self.accountName = self.accountName.strip(' ')
        self.isEntityRequired = bool(self.isEntityRequired)
        self.isHidden = bool(self.isHidden)
        self.isTaxable = bool(self.isTaxable)
        self.fundId = validate_uuid(self.fundId, throw=True)
        self.attributeId = validate_uuid(self.attributeId, throw=True)
        self.parentAccountId = validate_uuid(self.parentAccountId, throw=True)
        self.fsMappingId = validate_uuid(self.fsMappingId, throw=True)

        # default values for all new accounts
        self.state = "UNUSED"
        self.isHidden = False


@dataclass
class AccountPut:
    accountNo: str = None
    accountName: str = None
    accountDescription: str = None
    fsMappingId: str = None
    fsName: str = None
    isDryRun: bool = None
    parentAccountId: str = None
    attributeId: str = None
    isEntityRequired: bool = None
    isHidden: bool = None
    isTaxable: bool = None

    def __post_init__(self):
        self.accountName = (
            None if self.accountName is None else 
            self.accountName.strip(' ')
        )
        self.isEntityRequired = (
            None if self.isEntityRequired is None
            else bool(self.isEntityRequired)
        )
        self.accountNo = str(int(self.accountNo))
        self.isHidden = None if self.isHidden is None else bool(self.isHidden)
        self.isTaxable = None if self.isTaxable is None else bool(self.isTaxable)
        self.attributeId = validate_uuid(self.attributeId, throw=True)
        self.parentAccountId = validate_uuid(self.parentAccountId, throw=True)
        self.fsMappingId = validate_uuid(self.fsMappingId, throw=True)
