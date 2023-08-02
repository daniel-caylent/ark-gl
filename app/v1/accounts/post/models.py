"""Models for Accounts POST"""

from dataclasses import dataclass

# pylint: disable=import-error; Lambda layer dependency
from shared.dataclass_validators import (
    check_uuid,
    validate_int,
    validate_str,
    validate_bool,
)
# pylint: enable=import-error

@dataclass
class AccountPost:
    """Account POST model"""

    # pylint: disable=invalid-name; API standard
    fundId: str
    clientId: str
    attributeId: str
    accountNo: str
    accountName: str
    isTaxable: bool

    # optional
    fsName: str = None
    fsMappingId: str = None
    isEntityRequired: bool = False
    accountDescription: str = None
    parentAccountId: str = None
    fsMappingStatus: str = False
    # pylint: enable=invalid-name

    def __post_init__(self):
        # required
        self.accountNo = str(validate_int(self.accountNo, "accountNo", min_=100))
        self.accountName = validate_str(self.accountName, "accountName", min_len=3)
        self.fundId = check_uuid(self.fundId, "fundId")
        self.clientId = check_uuid(self.clientId, "clientId")
        self.attributeId = check_uuid(self.attributeId, "attributeId")
        self.isTaxable = validate_bool(self.isTaxable, "isTaxable")
        # optional

        self.fsName = (
            None if self. fsName is None
            else validate_str(self.fsName, "fsName")
        )
        self.isEntityRequired = bool(self.isEntityRequired)
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

        if self.fsMappingId == "00000000-0000-0000-0000-000000000000":
            self.fsMappingId = None
            self.fsMappingStatus = "SELF-MAPPED"
        elif self.fsMappingId is None:
            self.fsMappingStatus = "UNMAPPED"
        else:
            self.fsMappingStatus = "MAPPED"


@dataclass
class BulkAccountPost:
    """Model for bulk account POST"""

    # pylint: disable=invalid-name; API standard
    fundId: str
    clientId: str
    attributeId: str
    accountNo: str
    accountName: str
    isTaxable: bool

    # optional
    fsName: str = None
    fsMappingName: str = None
    isEntityRequired: bool = False
    accountDescription: str = None
    parentAccountName: str = None
    # pylint: enable=invalid-name

    def __post_init__(self):
        # required
        self.accountNo = str(validate_int(self.accountNo, "accountNo", min_=100))
        self.accountName = validate_str(self.accountName, "accountName", min_len=3)
        self.fundId = check_uuid(self.fundId, "fundId")
        self.clientId = check_uuid(self.clientId, "clientId")
        self.attributeId = check_uuid(self.attributeId, "attributeId")
        self.isTaxable = validate_bool(self.isTaxable, "isTaxable")
        # optional

        self.fsName = (
            None if self. fsName is None
            else validate_str(self.fsName, "fsName")
        )
        self.isEntityRequired = bool(self.isEntityRequired)
        self.parentAccountName = (
            None
            if self.parentAccountName is None
            else validate_str(self.parentAccountName, "parentAccountName")
        )
        self.fsMappingName = (
            None
            if self.fsMappingName is None
            else validate_str(self.fsMappingName, "fsMappingName")
        )
