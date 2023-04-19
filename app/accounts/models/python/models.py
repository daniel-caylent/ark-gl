from typing import Literal

from dataclasses import dataclass

@dataclass
class Account:
    accountNo: int
    accountName: str
    accountId: str
    accountDescription: str
    state: Literal["USED", "UNUSED", "ACTIVE"]
    isHidden: bool
    isTaxable: bool
    isVendorCustomerPartnerRequired: bool
    parrentAccountNo: int
    attributeNo: int

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
