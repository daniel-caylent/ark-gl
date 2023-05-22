#  pylint: disable-file=invalid-name
"""Models for the journal entries module"""

# journal entry models and line items models
from dataclasses import dataclass, field
from shared import validate_uuid


@dataclass
class JournalEntry:
    """Validate a journal entry from internal DB"""
    ledgerId: str
    journalEntryId: str
    reference: str
    memo: str
    adjustingJournalEntry: bool
    state: str
    isHidden: bool


@dataclass
class JournalEntryPost:
    """Validate journal entry data from a post"""
    ledgerId: str
    reference: str
    memo: str
    adjustingJournalEntry: bool
    state: str
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


@dataclass
class LineItem:
    """Validate an internal line item"""
    journalEntryId: str
    lineItemNo: str
    accountId: str
    memo: str
    isEntityRequired: bool
    amount: 10012
    type: str

    def __post_init__(self):
        self.type = validate_type(self.type)
        self.accountId = validate_uuid(self.accountId, "accountId")
        self.memo = validate_str(self.memo, "memo")
        self.isEntityRequired = validate_bool(self.isEntityRequired, "isEntityRequired")
        self.amount = validate_int(self.amount, "amount")


def validate_type(type_):
    """Validate the type of line item as 'CREDIT' or 'DEBIT'"""
    if type_ not in ["DEBIT", "CREDIT"]:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"Invalid line item type: {type}"
        )

    return type_


def check_uuid(uuid, name) -> str:
    """Validate a uuid"""
    if uuid is None:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"Required argument is missing: {name}."
        )

    try:
        validate_uuid(uuid, throw=True)
    except:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"{name} is not a valid UUID."
        )

    return uuid


def validate_bool(bool_, name):
    """Validate a boolean exists for this value"""
    if bool_ is None:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"Required argument is missing: {name}."
        )

    try:
        bool_ = bool(bool_)
    except:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"{name} is not a valid boolean."
        )
    return bool_


def validate_str(str_, name, min_len=0, max_len=255) -> str:
    """Validate a string exists for this value"""
    if str_ is None:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"Required argument is missing: {name}."
        )

    try:
        str_ = str_.strip()
    except:
        raise Exception(f"{name} is invalid.")  # pylint: disable=broad-exception-raised,raise-missing-from

    if len(str_) < min_len:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"{name} does not meet min length required of {min_len} characters."
        )
    if len(str_) > max_len:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"{name} does not meet max length required of {max_len} characters."
        )

    return str_


def validate_int(int_, name, allowed: list = None) -> int:
    """Validate an integer exists for this value"""

    if int_ is None:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"Required argument is missing: {name}."
        )

    try:
        int_ = int(str(int_))
    except:
        raise Exception(f"{name} is invalid.")  # pylint: disable=broad-exception-raised,raise-missing-from

    if allowed:
        if int_ not in allowed:
            raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
                f"{name} must be one of {allowed}."
            )

    return int_
