from dataclasses import dataclass, field
from shared.dataclass_validators import (
    check_uuid,
    validate_bool,
    validate_str
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
