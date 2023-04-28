from typing import Literal

from dataclasses import dataclass

@dataclass
class Account:
    accountNo: int
    accountName: str
    state: Literal["USED", "UNUSED", "ACTIVE"]
    accountDescription: str
    fsMappingId: str
    fsName: str
    isHidden: bool
    isTaxable: bool
    isVendorCustomerPartnerRequired: bool
    parentAccountId: str
    attributeId: str
    accountId: str
    fundId: str

    def __post_init__(self):
        self.isVendorCustomerPartnerRequired = bool(self.isVendorCustomerPartnerRequired)
        self.isHidden = bool(self.isHidden)
        self.isTaxable = bool(self.isTaxable)


@dataclass
class AccountPost:
    accountNo: int
    accountName: str
    accountDescription: str
    fsMappingId: str
    fsName: str
    isDryRun: bool
    parentAccountId: str
    attributeId: str
    fundId: str
    isVendorCustomerPartnerRequired: bool
    isHidden: bool = False
    isTaxable: bool = True
    state: Literal["USED", "UNUSED", "ACTIVE"] = "UNUSED"

    def __post_init__(self):
        self.accountName = self.accountName.strip(' ')
        self.isVendorCustomerPartnerRequired = bool(self.isVendorCustomerPartnerRequired)
        self.isHidden = bool(self.isHidden)
        self.isTaxable = bool(self.isTaxable)

