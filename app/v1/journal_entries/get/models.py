"""Models for JournalEntries GET"""

from dataclasses import dataclass, field


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
    date: str
    postDate: str
    isHidden: bool
    attachments: list = field(default_factory=list)
    lineItems: list = field(default_factory=list)
    # pylint: enable=invalid-name

    def __post_init__(self):
        self.adjustingJournalEntry = bool(self.adjustingJournalEntry)
        self.isHidden = bool(self.isHidden)
        self.date = str(self.date)
        self.postDate = str(self.postDate)
