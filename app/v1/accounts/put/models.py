from dataclasses import dataclass
from shared.dataclass_validators import (
    check_uuid,
    validate_bool,
    validate_int,
    validate_str,
)


@dataclass
class AccountPut:
    accountNo: str = None
    accountName: str = None
    accountDescription: str = None
    fsMappingId: str = None
    fsName: str = None
    isDryRun: bool = None
    parentAccountId: str = None
    attributeId: str = None
    isEntityRequired: bool = None
    isHidden: bool = None
    isTaxable: bool = None

    def __post_init__(self):
        self.accountName = (
            None if self.accountName is None else
            validate_str(self.accountName, "accountName", min_len=3)
        )
        self.isEntityRequired = (
            None if self.isEntityRequired is None
            else bool(self.isEntityRequired)
        )
        self.accountNo = (
            None if self.accountNo is None else
            str(validate_int(self.accountNo, "accountNo", min=100))
        )
        self.isHidden = (
            None if self.isHidden is None else
            validate_bool(self.isHidden, "isHidden")
        )
        self.isTaxable = (
            None if self.isTaxable is None else
            validate_bool(self.isTaxable, "isTaxable")
        )
        self.attributeId = (
            None if self.attributeId is None else
            check_uuid(self.attributeId, "attributeId")
        )
        self.parentAccountId = (
            None if self.parentAccountId is None else
            check_uuid(self.parentAccountId, "parentAccountId")
        )
        self.fsMappingId = (
            None if self.fsMappingId is None else
            check_uuid(self.fsMappingId, "fsMappingId")
        )
