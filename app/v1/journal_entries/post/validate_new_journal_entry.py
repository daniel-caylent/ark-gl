"""
Module that validates a journal entry
"""

# pylint: disable=import-error; Lambda layer dependency
from models import JournalEntryPost, LineItemPost, AttachmentPost
from arkdb import accounts, ledgers
from shared import dataclass_error_to_str
# pylint: enable=import-error


def validate_new_journal_entry(journal_entry):
    """
    Function that validates a journal entry

    journal_entry: dict
    Journal Entry object
    """
    # Check for missing details
    if journal_entry.get("ledgerId") is None:
        return 400, "No ledger specified.", None

    # validate the POST contents
    try:
        post = JournalEntryPost(**journal_entry)
    except Exception as e: # pylint: disable=broad-exception-caught; Unhandled exception not allowed
        return 400, dataclass_error_to_str(e), None

    if len(post.lineItems) == 0:
        return 400, "Journal entry is missing line items.", None

    # validate that the ledger exists
    ledger = ledgers.select_by_id(post.ledgerId)
    if ledger is None:
        return 400, "Specified ledger does not exist.", None

    accts = accounts.select_by_fund_id(ledger["fundId"])

    type_safe_line_items = []
    line_item_no = 0
    for item in post.lineItems:
        line_item_no += 1
        try:
            line_item_post = LineItemPost(**item)
            type_safe_line_items.append(
                {"lineItemNo": line_item_no, **line_item_post.__dict__}
            )
        except Exception as e: # pylint: disable=broad-exception-caught; Unhandled exception not allowed
            return 400, dataclass_error_to_str(e), None

        if not __validate_line_items_vs_accounts(type_safe_line_items, accts):
            return 400, "Line items are invalid", None

    post.lineItems = type_safe_line_items

    type_safe_attachments = []
    for attachment in post.attachments:
        try:
            attachment = AttachmentPost(**attachment)
            type_safe_attachments.append(attachment.__dict__)
        except Exception as e: # pylint: disable=broad-exception-caught; Unhandled exception not allowed
            return 400, dataclass_error_to_str(e), None

    post.attachments = type_safe_attachments

    if __sum_line_items(type_safe_line_items) != 0:
        return 400, "Line items do not sum to 0.", None

    __update_accounts_state(accts, [item["accountNo"] for item in type_safe_line_items])

    if ledger["state"] not in ["DRAFT", "POSTED"]:
        ledgers.update_by_id(ledger["ledgerId"], {"state": "DRAFT"})

    return 201, "", {"state": "DRAFT", **post.__dict__}


def __sum_line_items(line_items):
    """Sum all lines considering credit/debit"""
    total = 0
    for item in line_items:
        if item["type"] == "CREDIT":
            total += item["amount"]
        else:
            total -= item["amount"]
    return total

def __validate_line_items_vs_accounts(line_items, accts):
    """Check line-items account connection exists and have entity ids if required"""
    account_lookup = {}
    for acct in accts:
        account_lookup[acct["accountNo"]] = acct

    for line_item in line_items:
        acct = account_lookup.get(line_item["accountNo"])
        if not acct:
            return False

        if acct["isEntityRequired"]:
            if not line_item.get("entityId"):
                return False
    return True

def __update_accounts_state(accounts_, account_numbers):
    """Ensure accounts with line items are in DRAFT or POSTED state"""
    for account in accounts_:
        if account["accountNo"] in account_numbers:
            if account["state"] not in ["DRAFT", "POSTED"]:
                accounts.update_by_id(account["accountId"], {"state": "DRAFT"})
