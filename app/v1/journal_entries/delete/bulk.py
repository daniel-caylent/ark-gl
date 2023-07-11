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

    results = journal_entries.select_with_filter_paginated(valid_input)
    filtered_journal_entries = results["data"]

    delete_ids = []
    ledgers_dict = {}

    if not filtered_journal_entries:
        return 400, {"detail": "No journal entries match the search criteria."}

    for journal_entry in filtered_journal_entries:
        if journal_entry['state'] == 'POSTED':
            return 400, {'detail': f"POSTED journal entry cannot be deleted: {journal_entry['journalEntryId']}"}

        delete_ids.append(journal_entry["journalEntryId"])
        ledgers_dict[journal_entry["ledgerId"]] = None
    
    try:
        journal_entries.bulk_delete(delete_ids)
    except Exception as e:
        return 400, {"detail": f"Unable to delete: {str(e)}"}

    # update state for unused ledgers and accounts
    fund_ids = []
    for ledger_id in ledgers_dict:
        ledger = ledgers.select_by_id(ledger_id)
        ledgers_dict[ledger_id] = ledger
        fund_ids.append(ledger["fundId"])

    accounts_list = []
    for fund_id in set(fund_ids):
        accounts_list += accounts.select_by_fund_id(fund_id, translate=False)

    __update_unused_accounts(accounts_list)
    __update_unused_ledgers(ledgers_dict.values())

    return 200, {}


def __update_unused_accounts(accounts_: list):
    """Check to see if line items still exist for old accounts"""
    for acct in accounts_:
        line_items_count = accounts.get_line_items_count(acct["id"])
        if line_items_count == 0 and acct["state"] != "POSTED":
            print(f"Update unused account to UNUSED: {acct['uuid']}")
            accounts.update_by_id(acct["uuid"], {"state": "UNUSED"})

def __update_unused_ledgers(ledgers_list: list):
    """Replace ledger state with UNUSED if no journal entries exist for it"""
    for ledger in ledgers_list:
        journal_entries_ = journal_entries.select_by_ledger_id(ledger["ledgerId"])
        if len(journal_entries_) == 0:
            if ledger["state"] != "POSTED":
                ledgers.update_by_id(
                    ledger["ledgerId"],
                    {"state": "UNUSED"}
                )
            