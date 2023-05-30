from dataclasses import dataclass, field
from shared.dataclass_validators import (
    check_uuid,
    validate_bool,
    validate_str,
    validate_int
)

@dataclass
class JournalEntryPost:
    """Validate journal entry data from a post"""
    ledgerId: str
    date: str
    reference: str
    memo: str
    adjustingJournalEntry: bool
    journalEntryNo: int
    attachments: list = field(default_factory=list)
    lineItems: list = field(default_factory=list)
    isHidden: bool = False

    def __post_init__(self):
        self.ledgerId = check_uuid(self.ledgerId, "ledgerId")
        self.reference = validate_str(self.reference, "reference")
        self.memo = validate_str(self.memo, "memo")
        self.adjustingJournalEntry = validate_bool(
            self.adjustingJournalEntry, "adjustingJournalEntry"
        )
        self.isHidden = validate_bool(self.isHidden, "isHidden")


@dataclass
class LineItemPost:
    lineItemNo: int
    accountNo: str
    memo: str
    type: str
    amount: int
    entityId: str

    def __post_init__(self):
        self.lineItemNo = validate_int(self.lineItemNo, "lineItemNo")
        self.accountNo = validate_str(self.accountNo, "accountNo")
        self.memo = validate_str(self.memo, "memo")
        self.type = validate_str(self.type, "type", allowed=["CREDIT", "DEBIT"])
        self.amount = validate_int(self.amount, "amount")
        self.entityId = validate_str(self.entityId, "entityId")

@dataclass
class AttachmentPost:
    documentId: str
    documentMemo: str

    def __post_init__(self):
        self.documentId = validate_str(self.documentId, "documentId")
        self.documentMemo = validate_str(self.documentMemo, "documentMemo")
