"""Validations for Ledgers POST"""

# pylint: disable=import-error; Lambda layer dependency
from arkdb import ledgers
from models import LedgerPost
from shared import dataclass_error_to_str
# pylint: enable=import-error


def validate_new_ledger(ledger: dict) -> tuple[int, str, LedgerPost]:
    """Validate a new ledger against business rules"""

    # validate the POST contents
    try:
        post = LedgerPost(**ledger)
    except Exception as e:
        return 400, dataclass_error_to_str(e), None

    # get funds with the same name
    ledgers_ = ledgers.select_by_fund_id(post.fundId)
    unique = validate_unique_ledger(post, ledgers_)
    if unique is False:
        return 409, "Ledger name already exists in this fund.", None

    return 201, "", {"state": "UNUSED", **post.__dict__}


def validate_unique_ledger(ledger: LedgerPost, existing_ledgers):
    """Validate the incoming ledger has a unique name and number"""

    for e_ledger in existing_ledgers:
        if e_ledger["glName"].lower() == ledger.glName.lower():
            return False

    return True
