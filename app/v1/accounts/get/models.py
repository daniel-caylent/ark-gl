"""Models for Accounts GET"""
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Account:
    """Get account model"""
    # pylint: disable=invalid-name; API standard
    accountNo: str
    accountName: str
    state: str
    accountDescription: str
    fsMappingId: str
    fsName: str
    isTaxable: bool
    isEntityRequired: bool
    parentAccountId: str
    attributeId: str
    accountId: str
    fundId: str
    postDate: datetime
    fsMappingStatus: str
    # pylint: enable=invalid-name

    def __post_init__(self):
        self.isEntityRequired = bool(self.isEntityRequired)
        self.isTaxable = bool(self.isTaxable)
        self.postDate = None if self.postDate is None else self.postDate.strftime("%Y-%m-%dT%H:%M:%SZ")

        if self.fsMappingStatus == "SELF-MAPPED":
            self.fsMappingId = self.accountId
