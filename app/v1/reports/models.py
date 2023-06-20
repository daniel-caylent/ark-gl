from dataclasses import dataclass
from shared.dataclass_validators import validate_date, validate_list, validate_str

@dataclass
class ReportInputs:
    """Class to validate inputs for reports"""
    ledgerId: list
    journalEntryState: str = None
    startDate: str = None
    endDate: str = None

    def __post_init__(self):
        self.ledgerId = validate_list(self.ledgerId, "ledgerId", min_len=1, parse=True)
        self.journalEntryState = (
            None if self.journalEntryState is None
            else validate_str(self.journalEntryState, "journalEntryState",
                allowed=["UNUSED", "DRAFT", "POSTED"]
            )
        )
        self.startDate = (
            None if self.startDate is None else 
            validate_date(self.startDate, "startDate")
        )
        self.endDate = (
            None if self.endDate is None else
            validate_date(self.endDate, "endDate")
        )

