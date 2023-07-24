"""Lambda that will perform the PUT for JournalEntries"""

import json

# pylint: disable=import-error; Lambda layer dependency
from arkdb import accounts, journal_entries, ledgers
from shared import endpoint, validate_uuid, update_dict, dataclass_error_to_str
from models import JournalEntryPut, LineItemPost, AttachmentPost
# pylint: enable=import-error

COMMITED_CHANGEABLE = []
REQUIRED_FIELDS = ["date", "reference", "memo", "adjustingJournalEntry", "ledgerId"]


@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters
    if not event.get("pathParameters"):
        return 400, {"detail": "Missing path parameters"}

    journal_entry_id = event["pathParameters"].get("journalEntryId", None)
    if journal_entry_id is None:
        return 400, {"detail": "No journal entry specified."}

    if not validate_uuid(journal_entry_id):
        return 400, {"detail": "Invalid journal entry UUID."}

    # validate the request body
    try:
        body = json.loads(event["body"])
    except Exception:
        return 400, {"detail": "Body does not contain valid json."}

    if len(body.keys()) == 0:
        return 400, {"detail": "Body does not contain content."}

    # validate the PUT contents
    try:
        put = JournalEntryPut(**body)
    except Exception as e:
        return 400, {"detail": dataclass_error_to_str(e)}

    # verify journal entry exists
    journal_entry = journal_entries.select_by_id(journal_entry_id, translate=False)
    if journal_entry is None:
        return 404, {"detail": "No journal entry found."}

    ledgers_list = []
    if put.ledgerId:
        ledger = ledgers.select_by_id(put.ledgerId, translate=False)
        ledgers_list.append(ledgers.select_by_id(journal_entry["ledger_id"], translate=False))
    else:
        # verify ledger exists
        ledger = ledgers.select_by_id(journal_entry["ledger_id"], translate=False)
    
    ledgers_list.append(ledger)
    if not ledger:
        return 400, {"detail": "Supplied ledger ID does not match an existing ledger."}

    if journal_entry['state'] == 'POSTED':
        for key in body.keys():
            if key not in COMMITED_CHANGEABLE:
                return 400, {'detail': f"POSTED ledger property cannot be modified: {key}."}

    # Validate that line items reference real accounts within the fund
    accts = accounts.select_by_fund_id(ledger["fund_entity_id"], translate=False)
    type_safe_line_items = []
    if put.lineItems:
        line_item_no = 0
        for item in put.lineItems:
            line_item_no += 1
            try:
                line_item_put = LineItemPost(**item)
                type_safe_line_items.append(line_item_put.__dict__)
            except Exception as e:
                return 400, {"detail": dataclass_error_to_str(e)}

        put.lineItems = type_safe_line_items

    type_safe_attachments = []
    if put.attachments:
        for attachment in put.attachments:
            try:
                attachment = AttachmentPost(**attachment)
                type_safe_attachments.append(attachment.__dict__)
            except Exception as e:
                return 400, {"detail": dataclass_error_to_str(e)}

        put.attachments = type_safe_attachments

    # only keep fields present in the initial body, but replace
    # with type safe values from dataclass
    type_safe_body = update_dict(body, put.__dict__)

    line_items = type_safe_body.get('lineItems')
    if line_items:
        if __sum_line_items(line_items) != 0:
            return 400, {"detail": "Line items do not sum to zero."}
        if len(line_items) == 0:
            return 400, {"detail": "Line items cannot be an empty array."}

        valid, reason = __validate_line_items_vs_accounts(line_items, accts)
        if not valid:
            return 400, {"detail": reason}

    missing = check_missing_fields(type_safe_body, REQUIRED_FIELDS)
    if missing is not None:
        return 400, {"detail": f"{missing} cannot be null."}

    old_line_items = journal_entries.get_line_items(journal_entry["id"])
    journal_entries.update_by_id(journal_entry_id, type_safe_body)

    if put.ledgerId:
        __update_ledgers_state(ledgers_list)
    if line_items:
        __update_draft_accounts(accts, [item["accountId"] for item in line_items])
        __update_unused_accounts(accts, old_line_items)

    return 200, {}


def check_missing_fields(dict_, required):
    """
    Check that the ledger information about to be updated does not input
    any null values for required fields
    """
    keys = list(dict_.keys())
    for field in required:
        if field in keys:
            value = dict_[field]

            if value is None:
                return field

    return None

def __update_ledgers_state(ledgers_: list):
    """Replace ledger state with UNUSED or DRAFT depending on circumstances"""
    for ledger in ledgers_:
        journal_entries_ = journal_entries.select_by_ledger_id(ledger["uuid"])

        if journal_entries_ and ledger["state"] not in ["POSTED", "DRAFT"]:
            ledgers.update_by_id(
                ledger["uuid"],
                {"state": "DRAFT"}
            )
        elif not journal_entries_ and ledger["state"] not in ["POSTED", "UNUSED"]:
            ledgers.update_by_id(
                ledger["uuid"],
                {"state": "UNUSED"}
            )

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
        account_lookup[acct["uuid"]] = acct

    for line_item in line_items:
        acct = account_lookup.get(line_item["accountId"])
        if not acct:
            return False, f"Line item references invalid account: {line_item['accountId']}"

        if bool(acct["is_entity_required"]) is True:
            if not line_item.get("entityId"):
                return False, f"Line items for account require entityId: {line_item['accountId']}"
    return True, None

def __update_draft_accounts(accounts_, account_ids):
    """Ensure accounts with line items are in DRAFT or POSTED state"""
    for account in accounts_:
        if account["uuid"] in account_ids:
            if account["state"] not in ["DRAFT", "POSTED"]:
                accounts.update_by_id(account["uuid"], {"state": "DRAFT"})

def __update_unused_accounts(accounts_, line_items):
    """Check to see if line items still exist for old accounts"""
    account_lookup = {}
    for acct in accounts_:
        account_lookup[acct["uuid"]] = acct

    for item in line_items:
        acct = account_lookup.get(item["accountId"])
        if acct is not None:
            line_items = accounts.get_line_items(acct["uuid"])

            if len(line_items) == 0 and acct["state"] != "POSTED":
                accounts.update_by_id(acct["uuid"], {"state": "UNUSED"})
