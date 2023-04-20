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
    parrentAccountNo: int
    attributeNo: int
    accountId: str

#post
class AccountPost:
    accountNo: int
    accountName: str
    state: Literal["USED", "UNUSED", "ACTIVE"] = "UNUSED"
    accountDescription: str
    fsMappingId: str
    fsName: str
    isTaxable: bool
    isVendorCustomerPartnerRequired: bool
    isDryRun: bool
    parentAccountNo: int
    attributeNo: int

    def __post_init__(self):
        self.accountNo = int(self.accountNo)
        self.attributeNo = int(self.attributeNo)
        self.parrentAccountNo = int(self.parrentAccountNo)
        self.accountName = self.accountName.strip(' ')

