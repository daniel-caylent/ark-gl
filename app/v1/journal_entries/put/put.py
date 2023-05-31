import json

from arkdb import accounts, journal_entries, ledgers
from shared import (
    endpoint,
    validate_uuid,
    update_dict,
    dataclass_error_to_str
  )
from models import JournalEntryPut, LineItemPost, AttachmentPost

COMMITED_CHANGEABLE = []
REQUIRED_FIELDS = [    
    'date', 'reference', 'memo', 'adjustingJournalEntry'
]

@endpoint
def handler(event, context) -> tuple[int, dict]:
    if not event.get('pathParameters'):
        return 400, {'detail': "Missing path parameters"}

    journal_entry_id = event['pathParameters'].get('journalEntryId', None)
    if journal_entry_id is None:
        return 400, {'detail': "No journal entry specified."}

    if not validate_uuid(journal_entry_id):
        return 400, {'detail': "Invalid journal entry UUID."}

    # validate the request body
    try:
        body = json.loads(event['body'])
    except:
        return 400, {'detail': "Body does not contain valid json."}

    if len(body.keys()) == 0:
        return 400, {'detail': "Body does not contain content."}

    # validate the PUT contents
    try:
        put = JournalEntryPut(**body)
    except Exception as e:
        return 400, {'detail': dataclass_error_to_str(e)}


    # verify journal entry exists
    journal_entry = journal_entries.select_by_id(journal_entry_id)
    if journal_entry is None:
        return 404, {"detail": "No journal entry found."}

    # verify ledger exists
    ledger = ledgers.select_by_id(journal_entry["ledgerId"])

    if journal_entry['state'] == 'COMMITTED':
        for key in body.keys():
            if key not in COMMITED_CHANGEABLE:
                return 400, {'detail': f"COMMITTED ledger property cannot be modified: {key}."}

    # Validate that line items reference real accounts within the fund
    accts = accounts.select_by_fund_id(ledger["fundId"])
    acct_numbers = [acct["accountNo"] for acct in accts]
    type_safe_line_items = []
    if put.lineItems:
        line_item_no = 0
        for item in put.lineItems:
            line_item_no += 1
            try:
                line_item_put = LineItemPost(**item)
                type_safe_line_items.append({"lineItemNo": line_item_no, **line_item_put.__dict__})
            except Exception as e:
                return 400, {"detail": dataclass_error_to_str(e)}

            if line_item_put.accountNo not in acct_numbers:
                return 400, {"detail": f"Line item references invalid account. Line item number: {line_item_put.lineItemNo}"}

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


    if sum_line_items(put.lineItems) != 0:
        return 400, {"detail": "Line items do not sum to 0."}

    # only keep fields present in the initial body, but replace
    # with type safe values from dataclass
    type_safe_body = update_dict(body, put.__dict__)

    missing = check_missing_fields(type_safe_body, REQUIRED_FIELDS)
    if missing is not None:
        return 400, {'detail': f"{missing} cannot be null or empty."}

    journal_entries.update_by_id(journal_entry_id, type_safe_body)
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

            if value is None or value == '':
                return field
    
    return None

def sum_line_items(line_items):
    sum = 0
    for item in line_items:
        if item["type"] == "CREDIT":
            sum += item["amount"]
        else:
            sum -= item["amount"]

    return sum
