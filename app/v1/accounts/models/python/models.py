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
    parentAccountNo: int
    attributeNo: int
    accountId: str
    fundId: str

#post
@dataclass
class AccountPost:
    accountNo: int
    accountName: str
    accountDescription: str
    fsMappingId: str
    fsName: str
    isDryRun: bool
    parentAccountNo: int
    attributeId: int
    fundId: str
    isVendorCustomerPartnerRequired: bool
    isHidden: bool = False
    isTaxable: bool = True
    state: Literal["USED", "UNUSED", "ACTIVE"] = "UNUSED"

    def __post_init__(self):
        self.accountNo = int(self.accountNo)
        self.attributeId = int(self.attributeId)
        self.parentAccountNo = int(self.parentAccountNo)
        self.accountName = self.accountName.strip(' ')

