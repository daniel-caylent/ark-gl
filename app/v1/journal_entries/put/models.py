from dataclasses import dataclass
from shared.dataclass_validators import validate_str, validate_bool

@dataclass
class JournalEntryPut:
    """Validate journal entry data from a put"""
    reference: str = None
    memo: str = None
    adjustingJournalEntry: bool = None
    state: str = None
    lineItems: list = None
    isHidden: bool = None

    def __post_init__(self):
        self.reference = (
            None
            if self.reference is None
            else validate_str(self.reference, "reference")
        )
        self.memo = None if self.memo is None else validate_str(self.memo, "memo")
        self.adjustingJournalEntry = (
            None
            if self.adjustingJournalEntry is None
            else validate_bool(self.adjustingJournalEntry, "adjustingJournalEntry")
        )
