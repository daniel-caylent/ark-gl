"""Models for JournalEntries PUT"""

from dataclasses import dataclass

# pylint: disable=import-error; Lambda layer dependency
from shared.dataclass_validators import (
    validate_str, validate_bool, validate_int, check_uuid
)
# pylint: enable=import-error;

@dataclass
class JournalEntryPut:
    """Validate journal entry data from a put"""

    # pylint: disable=invalid-name; API standard
    ledgerId: str = None
    reference: str = None
    memo: str = None
    adjustingJournalEntry: bool = None
    lineItems: list = None
    attachments: list = None
    date: str = None
    # pylint: enable=invalid-name;

    def __post_init__(self):
        self.ledgerId = (
            None if self.ledgerId is None else
            check_uuid(self.ledgerId, "ledgerId")
        )
        self.reference = (
            None if self.reference is None else
            validate_str(self.reference, "reference")
        )
        self.memo = (
            None if self.memo is None else
            validate_str(self.memo, "memo")
        )
        self.adjustingJournalEntry = (
            None
            if self.adjustingJournalEntry is None
            else validate_bool(self.adjustingJournalEntry, "adjustingJournalEntry")
        )
        self.date = None if self.date is None else validate_str(self.date, "date")


@dataclass
class LineItemPost:
    # pylint: disable=invalid-name; API standard
    accountId: str
    memo: str
    type: str
    amount: int
    entityId: str = None
    # pylint: enable=invalid-name;

    def __post_init__(self):
        self.accountId = check_uuid(self.accountId, "accountId")
        self.memo = validate_str(self.memo, "memo")
        self.type = validate_str(self.type, "type", allowed=["CREDIT", "DEBIT"])
        self.amount = validate_int(self.amount, "amount", min_=0)
        self.entityId = None if self.entityId is None else check_uuid(self.entityId, "entityId")


@dataclass
class AttachmentPost:

    # pylint: disable=invalid-name; API standard
    documentId: str
    documentMemo: str
    # pylint: enable=invalid-name

    def __post_init__(self):
        self.documentId = validate_str(self.documentId, "documentId", min_len=1, max_len=64)
        self.documentMemo = validate_str(self.documentMemo, "documentMemo")
