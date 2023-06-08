"""Validations for Ledgers POST"""

# pylint: disable=import-error; Lambda layer dependency
from arkdb import funds, ledgers
from models import LedgerPost
# pylint: enable=import-error


def validate_new_ledger(ledger: dict) -> tuple[int, str, LedgerPost]:
    """Validate a new ledger against business rules"""

    # validate the POST contents
    try:
        post = LedgerPost(**ledger)
    except Exception as e:
        remove_str = "__init__() got an "
        error_str = str(e).replace(remove_str, "")
        remove_str = "__init__() "
        error_str = str(e).replace(remove_str, "")

        return 400, error_str[0].upper() + error_str[1:], None

    # validate that the fund exists and client has access to it
    fund = funds.select_by_uuid(post.fundId)
    if fund is None:
        return 400, "Specified fund does not exist.", None

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
