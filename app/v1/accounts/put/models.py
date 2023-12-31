"""Models for Accounts PUT"""

from dataclasses import dataclass

# pylint: disable=import-error; Lambda layer dependency
from shared.dataclass_validators import (
    check_uuid,
    validate_bool,
    validate_int,
    validate_str,
)
# pylint: enable=import-error


@dataclass
class AccountPut:
    """Model for account PUT"""

    # pylint: disable=invalid-name; API standard
    accountNo: str = None
    accountName: str = None
    accountDescription: str = None
    fsMappingId: str = None
    fsName: str = None
    parentAccountId: str = None
    attributeId: str = None
    isEntityRequired: bool = None
    isTaxable: bool = None
    fsMappingStatus: str = None
    # pylint: enable=invalid-name

    def __post_init__(self):
        self.accountName = (
            None
            if self.accountName is None
            else validate_str(self.accountName, "accountName", min_len=3)
        )
        self.isEntityRequired = (
            None if self.isEntityRequired is None else bool(self.isEntityRequired)
        )
        self.accountNo = (
            None
            if self.accountNo is None
            else str(validate_int(self.accountNo, "accountNo", min_=100))
        )
        self.isTaxable = (
            None
            if self.isTaxable is None
            else validate_bool(self.isTaxable, "isTaxable")
        )
        self.attributeId = (
            None
            if self.attributeId is None
            else check_uuid(self.attributeId, "attributeId")
        )
        self.parentAccountId = (
            None
            if self.parentAccountId is None
            else check_uuid(self.parentAccountId, "parentAccountId")
        )
        self.fsMappingId = (
            None
            if self.fsMappingId is None
            else check_uuid(self.fsMappingId, "fsMappingId")
        )
        self.fsName = (
            None if self. fsName is None
            else validate_str(self.fsName, "fsName")
        )

    def update_fs(self):
        """Update the fsMappingStatus based on input uuid"""
        if self.fsMappingId == "00000000-0000-0000-0000-000000000000":
            self.fsMappingStatus = "SELF-MAPPED"
            self.fsMappingId = None
        elif self.fsMappingId is None:
            self.fsMappingStatus = "UNMAPPED"
        else:
            self.fsMappingStatus = "MAPPED"
