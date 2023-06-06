from dataclasses import dataclass
from shared.dataclass_validators import (
    validate_str, validate_bool, validate_int, check_uuid
)

@dataclass
class JournalEntryPut:
    """Validate journal entry data from a put"""
    reference: str = None
    memo: str = None
    adjustingJournalEntry: bool = None
    lineItems: list = None
    attachments: list = None
    isHidden: bool = None
    date: str = None

    def __post_init__(self):
        self.reference = (
            None if self.reference is None else
            validate_str(self.reference, "reference", min_len=1)
        )
        self.memo = (
            None if self.memo is None else
            validate_str(self.memo, "memo", min_len=1)
        )
        self.adjustingJournalEntry = (
            None if self.adjustingJournalEntry is None 
            else validate_bool(self.adjustingJournalEntry, "adjustingJournalEntry")
        )
        self.isHidden = (
            None if self.isHidden is None else
            validate_bool(self.isHidden, "isHidden")
        )
        self.date = (
            None if self.date is None else validate_str(self.date, "date")
        )


@dataclass
class LineItemPost:
    accountNo: str
    memo: str
    type: str
    amount: int
    entityId: str

    def __post_init__(self):
        self.accountNo = validate_str(self.accountNo, "accountNo")
        self.memo = validate_str(self.memo, "memo")
        self.type = validate_str(self.type, "type", allowed=["CREDIT", "DEBIT"])
        self.amount = validate_int(self.amount, "amount", min=0)
        self.entityId = check_uuid(self.entityId, "entityId")


@dataclass
class AttachmentPost:
    documentId: str
    documentMemo: str

    def __post_init__(self):
        self.documentId = validate_str(self.documentId, "documentId", min_len=1, max_len=64)
        self.documentMemo = validate_str(self.documentMemo, "documentMemo")
