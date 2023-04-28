from typing import Literal

from dataclasses import dataclass

@dataclass
class Account:
    id: int
    accountNo: int
    accountName: str
    state: Literal["USED", "UNUSED", "ACTIVE"]
    accountDescription: str
    fsMappingId: str
    fsName: str
    isHidden: bool
    isTaxable: bool
    isVendorCustomerPartnerRequired: bool
    parentAccountNo: int
    attributeId: str
    accountId: str
    fundId: str


@dataclass
class AccountPost:
    accountNo: int
    accountName: str
    accountDescription: str
    fsMappingId: str
    fsName: str
    isDryRun: bool
    parentAccountNo: int
    attributeId: str
    fundId: str
    isVendorCustomerPartnerRequired: bool
    isHidden: bool = False
    isTaxable: bool = True
    state: Literal["USED", "UNUSED", "ACTIVE"] = "UNUSED"

    def __post_init__(self):
        self.accountName = self.accountName.strip(' ')
        self.isVendorCustomerPartnerRequired = bool(self.isVendorCustomerPartnerRequired)

