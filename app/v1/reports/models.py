from dataclasses import dataclass, field
from shared.dataclass_validators import validate_date, validate_list, validate_str, check_uuid

@dataclass
class ReportInputs:
    """Class to validate inputs for reports"""
    ledgerIds: list = None
    attributeIds: list = None
    accountIds: list = None
    journalEntryState: str = None
    startDate: str = None
    endDate: str = None

    def __post_init__(self):
        self.ledgerIds = None if self.ledgerIds is None else validate_list(self.ledgerIds, "ledgerId")
        self.attributeIds = None if self.attributeIds is None else validate_list(self.attributeIds, "attributeIds")
        self.accountIds = None if self.accountIds is None else validate_list(self.accountIds, "accountIds")
        self.journalEntryState = (
            None if self.journalEntryState is None
            else validate_str(self.journalEntryState, "journalEntryState",
                allowed=["UNUSED", "DRAFT", "POSTED"]
            )
        )
        self.startDate = (
            None if self.startDate is None else 
            validate_date(self.startDate, "startDate")
        )
        self.endDate = (
            None if self.endDate is None else
            validate_date(self.endDate, "endDate")
        )

        if self.ledgerIds:
            for id_ in self.ledgerIds:
                check_uuid(id_, f"ledgerId: {id_}")
        if self.accountIds:
            for id_ in self.accountIds:
                check_uuid(id_, f"accountId: {id_}")
        if self.attributeIds:
            for id_ in self.attributeIds:
                check_uuid(id_, f"attributeId: {id_}")

        if not (self.ledgerIds or self.accountIds):
            raise Exception("Search criteria is too broad. Include one of: accountIds or ledgerIds")

@dataclass
class TrialBalanceAccount:
    accountId: str
    accountName: str
    accountNo: str
    parentAccountId: str
    state: str
    fsMappingId: str
    fsName: str
    isTaxable: bool
    isEntityRequired: bool
    attributeId: str
    accountType: str
    detailType: str
    postDate: str
    fundId: str
    fsMappingStatus: str
    totalAmount: int = 0
    lineItems: list = field(default_factory=lambda: [])

    def __post_init__(self):
        self.isTaxable = bool(self.isTaxable)
        self.isEntityRequired = bool(self.isEntityRequired)

        if self.fsMappingStatus == "SELF-MAPPED":
            self.fsMappingId = self.accountId
