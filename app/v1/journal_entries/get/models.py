"""Models for JournalEntries GET"""
from datetime import datetime

from dataclasses import dataclass, field

from shared.dataclass_validators import validate_str, validate_bool


@dataclass
class JournalEntry:
    """Validate a journal entry from internal DB"""

    # pylint: disable=invalid-name; API standard
    ledgerId: str
    journalEntryId: str
    journalEntryNum: str
    reference: str
    memo: str
    adjustingJournalEntry: bool
    state: str
    date: datetime
    postDate: str
    currencyName: str
    currencyDecimal: int
    fundId: str

    attachments: list = field(default_factory=list)
    lineItems: list = field(default_factory=list)
    # pylint: enable=invalid-name

    def __post_init__(self):
        self.adjustingJournalEntry = bool(self.adjustingJournalEntry)
        self.postDate = None if self.postDate is None else self.postDate.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.date = self.date.strftime("%Y-%m-%d")

@dataclass
class SortItem:
    """Validate sort item"""
    name: str
    descending: bool

    def __post_init__(self):
        self.name = validate_str(self.name, "name", allowed=[
            "fundId", "ledgerName", "journalEntryNum", "date",
            "debits", "credits", "accountNo",
            "accountName", "entityId", "state"
        ])
        self.descending = validate_bool(self.descending, "descending", strict=True)
