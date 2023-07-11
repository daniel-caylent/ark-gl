"""Lambda that will perform the bulk DELETE for JournalEntries"""

# pylint: disable=import-error; Lambda layer dependency
from arkdb import accounts, journal_entries, ledgers
from shared import endpoint, validate_uuid, dataclass_error_to_str

from models import FilterInput
# pylint: disable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters
    """Handler for the bulk delete for journal entries"""
    if not event.get("queryStringParameters"):
        return 400, {"detail": "Missing query string parameters."}

    filter = event.get("queryStringParameters")

    try:
        valid_input = FilterInput(**filter).__dict__
    except Exception as e:
        return 400, {"detail": dataclass_error_to_str(e)}

    filtered_journal_entries = journal_entries.select_with_filter_paginated(valid_input)

    delete_ids = []
    for journal_entry in filtered_journal_entries:
        if journal_entry['state'] == 'POSTED':
            return 400, {'detail': "POSTED journal entry cannot be deleted."}

        delete_ids.append(journal_entry["journalEntryId"])
    
    try:
        journal_entries.bulk_delete(delete_ids)
    except Exception as e:
        return 400, {"detail": f"Unable to delete: {str(e)}"}

    # ledger = ledgers.select_by_id(journal_entry["ledger_id"])
    # accts = accounts.select_by_fund_id(ledger["fundId"], translate=False)

    # __update_unused_accounts(accts, line_items)
    # __update_unused_ledger(ledger)

    return 200, {}


def __update_unused_accounts(accounts_, line_items):
    """Check to see if line items still exist for old accounts"""
    account_lookup = {}
    for acct in accounts_:
        account_lookup[acct["uuid"]] = acct

    for item in line_items:
        acct = account_lookup.get(item["accountId"])
        if acct is not None:
            line_items = accounts.get_line_items(acct["id"])
            if len(line_items) == 0 and acct["state"] != "POSTED":
                accounts.update_by_id(acct["uuid"], {"state": "UNUSED"})

def __update_unused_ledger(ledger):
    """Replace ledger state with UNUSED if no journal entries exist for it"""
    journal_entries_ = journal_entries.select_by_ledger_id(ledger["ledgerId"])
    if len(journal_entries_) == 0:
        if ledger["state"] != "POSTED":
            ledgers.update_by_id(
                ledger["ledgerId"],
                {"state": "UNUSED"}
            )
    
            