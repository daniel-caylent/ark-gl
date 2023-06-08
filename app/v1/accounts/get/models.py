"""Models for Accounts GET"""

from dataclasses import dataclass


@dataclass
class Account:
    accountNo: str
    accountName: str
    state: str
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
