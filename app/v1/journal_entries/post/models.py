"""Models for JournalEntries POST"""

from dataclasses import dataclass, field

# pylint: disable=import-error; Lambda layer dependency
from shared.dataclass_validators import (
    check_uuid,
    validate_bool,
    validate_str,
    validate_int,
    validate_date,
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
    journalEntryNum: int = None
    attachments: list = field(default_factory=list)
    # pylint: enable=invalid-name;

    def __post_init__(self):
        self.ledgerId = check_uuid(self.ledgerId, "ledgerId")
        self.reference = validate_str(self.reference, "reference")
        self.memo = validate_str(self.memo, "memo")
        self.adjustingJournalEntry = validate_bool(
            self.adjustingJournalEntry, "adjustingJournalEntry"
        )
        self.date = validate_date(self.date, "date", "%Y-%m-%d")
        self.journalEntryNum = (
            None
            if self.journalEntryNum is None
            else validate_int(self.journalEntryNum, "journalEntryNum")
        )


@dataclass
class LineItemPost:
    """Line Item POST model"""

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
        self.entityId = (
            None if self.entityId is None else check_uuid(self.entityId, "entityId")
        )


@dataclass
class AttachmentPost:
    """Attachment POST model"""

    # pylint: disable=invalid-name; API standard
    documentId: str
    documentMemo: str
    # pylint: enable=invalid-name

    def __post_init__(self):
        self.documentId = validate_str(
            self.documentId, "documentId", min_len=1, max_len=64
        )
        self.documentMemo = validate_str(self.documentMemo, "documentMemo")


@dataclass
class BulkJournalEntryPost:
    """Model for bulk journal entries"""

    # pylint: disable=invalid-name; API standard
    fundId: str
    clientId: str
    ledgerName: str
    date: str
    reference: str
    memo: str
    adjustingJournalEntry: str
    lineItems: list
    journalEntryNum: str = None
    attachments: list = field(default_factory=list)
    # pylint: enable=invalid-name

    def __post_init__(self):
        self.fundId = check_uuid(self.fundId, "ledgerId")
        self.clientId = check_uuid(self.clientId, "ledgerId")
        self.ledgerName = validate_str(self.ledgerName, "ledgerName")
        self.reference = validate_str(self.reference, "reference")
        self.memo = validate_str(self.memo, "memo")
        self.adjustingJournalEntry = validate_bool(
            self.adjustingJournalEntry, "adjustingJournalEntry"
        )
        self.date = validate_date(self.date, "date", "%Y-%m-%d")
        self.journalEntryNum = (
            None
            if self.journalEntryNum is None
            else validate_int(self.journalEntryNum, "journalEntryNum")
        )


@dataclass
class BulkLineItemPost:
    """Line Item POST model"""

    # pylint: disable=invalid-name; API standard
    accountId: str
    memo: str
    type: str
    amount: float
    decimals: int
    entityId: str = None
    # pylint: enable=invalid-name;

    def __post_init__(self):
        self.accountId = check_uuid(self.accountId, "accountId")
        self.memo = validate_str(self.memo, "memo")
        self.type = validate_str(self.type, "type", allowed=["CREDIT", "DEBIT"])
        self.amount = validate_int(
            self.convert_amount(self.amount, self.decimals), "amount", min_=0
        )
        self.entityId = (
            None if self.entityId is None else check_uuid(self.entityId, "entityId")
        )

    @staticmethod
    def convert_amount(amount: float, decimals: int):
        """Convert floating point amounts to integers"""
        try:
            if decimals > 0:
                amount = float(amount)
        except Exception as e:
            raise Exception(f"Invalid amount for line item: {amount}") from e

        amount_str = str(amount)
        split_amount = amount_str.split(".")

        if len(split_amount) == 1:
            split_amount.append("")

        dollars = split_amount[0]
        cents = split_amount[1]

        if len(cents) > decimals:
            raise Exception(f"Line item amount has too many decimals: {amount}")

        if len(cents) < decimals:
            dif = decimals - len(cents)
            cents = cents + "0" * dif

        return int(dollars + cents)
