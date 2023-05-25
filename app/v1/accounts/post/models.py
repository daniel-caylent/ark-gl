from dataclasses import dataclass

from shared.dataclass_validators import (
    check_uuid,
    validate_int,
    validate_str,
    validate_bool
)

@dataclass
class AccountPost:
    fundId: str = None
    attributeId: str = None
    accountNo: str = None
    accountName: str = None
    isTaxable: bool = None
    fsName: str = None

    # optional
    fsMappingId: str = None
    isEntityRequired: bool = False
    accountDescription: str = None
    isDryRun: bool = False
    parentAccountId: str = None
    isHidden: bool = False

    def __post_init__(self):
        # required
        self.accountNo = str(validate_int(self.accountNo, "accountNo", min=100))
        self.accountName = validate_str(self.accountName, "accountName", min_len=3)
        self.fundId = check_uuid(self.fundId, "fundId")
        self.attributeId = check_uuid(self.attributeId, "attributeId")
        self.isTaxable = validate_bool(self.isTaxable, "isTaxable")
        self.fsName = validate_str(self.fsName, "fsName", min_len=3)

        # optional
        self.isEntityRequired = bool(self.isEntityRequired)
        self.isHidden = bool(self.isHidden)
        self.parentAccountId = (
            None if self.parentAccountId is None else
            check_uuid(self.parentAccountId, "parentAccountId")
        )
        self.fsMappingId = (
            None if self.fsMappingId is None else
            check_uuid(self.fsMappingId, "fsMappingId")
        )
