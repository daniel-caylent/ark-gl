"""Models for JournalEntries POST"""

from dataclasses import dataclass, field

# pylint: disable=import-error; Lambda layer dependency
from shared.dataclass_validators import (
    check_uuid,
    validate_bool,
    validate_str,
    validate_int,
)
# pylint: enable=import-error

@dataclass
class JournalEntryPost:
    """Validate journal entry data from a post"""

    # pylint: disable=invalid-name; API standard
    ledgerId: str
    date: str
    reference: str
    memo: str
    adjustingJournalEntry: bool
    lineItems: list
    attachments: list = field(default_factory=list)
    isHidden: bool = False
    # pylint: enable=invalid-name;

    def __post_init__(self):
        self.ledgerId = check_uuid(self.ledgerId, "ledgerId")
        self.reference = validate_str(self.reference, "reference", max_len=64)
        self.memo = validate_str(self.memo, "memo")
        self.adjustingJournalEntry = validate_bool(
            self.adjustingJournalEntry, "adjustingJournalEntry"
        )
        self.isHidden = validate_bool(self.isHidden, "isHidden")


@dataclass
class LineItemPost:
    """Line Item POST model"""

    # pylint: disable=invalid-name; API standard
    accountNo: str
    memo: str
    type: str
    amount: int
    entityId: str = None
    # pylint: enable=invalid-name;

    def __post_init__(self):
        self.accountNo = validate_str(self.accountNo, "accountNo")
        self.memo = validate_str(self.memo, "memo")
        self.type = validate_str(self.type, "type", allowed=["CREDIT", "DEBIT"])
        self.amount = validate_int(self.amount, "amount", min_=0)
        self.entityId = None if self.entityId is None else validate_str(self.entityId, "entityId")


@dataclass
class AttachmentPost:
    """Attachment POST model"""

    # pylint: disable=invalid-name; API standard
    documentId: str
    documentMemo: str
    # pylint: enable=invalid-name

    def __post_init__(self):
        self.documentId = validate_str(self.documentId, "documentId", min_len=1, max_len=64)
        self.documentMemo = validate_str(self.documentMemo, "documentMemo")
