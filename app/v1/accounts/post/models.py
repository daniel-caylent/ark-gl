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
    isDryRun: bool = False
    parentAccountId: str = None
    isHidden: bool = False
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
            else validate_str(self.fsName, "fsName", min_len=3)
        )
        self.isEntityRequired = bool(self.isEntityRequired)
        self.isHidden = bool(self.isHidden)
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
