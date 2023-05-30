from dataclasses import dataclass
from shared.dataclass_validators import (
    validate_str, validate_bool, validate_int
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
            None if self.reference is None else validate_str(self.reference, "reference")
        )
        self.memo = (
            None if self.memo is None else validate_str(self.memo, "memo")
        )
        self.adjustingJournalEntry = (
            None if self.adjustingJournalEntry is None 
            else validate_bool(self.adjustingJournalEntry, "adjustingJournalEntry")
        )
        self.isHidden = (
            None if self.isHidden is None else validate_bool(self.isHidden, "isHidden")
        )
        self.date = (
            None if self.date is None else validate_str(self.date, "date")
        )


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
