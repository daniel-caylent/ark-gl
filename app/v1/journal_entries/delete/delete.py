"""Lambda that will perform the DELETE for JournalEntries"""

# pylint: disable=import-error; Lambda layer dependency
from arkdb import accounts, journal_entries, ledgers
from shared import endpoint, validate_uuid
# pylint: disable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters
    if not event.get("pathParameters"):
        return 400, {"detail": "Missing path parameters"}

    journal_entry_id = event["pathParameters"].get("journalEntryId", None)
    if journal_entry_id is None:
        return 400, {"detail": "No journal entry specified."}

    if not validate_uuid(journal_entry_id):
        return 400, {"detail": "Invalid UUID provided."}

    journal_entry = journal_entries.select_by_id(journal_entry_id)
    if journal_entry is None:
        return 404, {"detail": "No journal entry found."}

    if journal_entry['state'] == 'POSTED':
        return 400, {'detail': "POSTED journal entry cannot be deleted."}

    line_items = journal_entries.get_line_items(journal_entry_id)
    try:
        journal_entries.delete_by_id(journal_entry_id)
    except Exception as e:
        return 400, {"detail": f"Unable to delete: {str(e)}"}

    ledger = ledgers.select_by_id(journal_entry["ledgerId"])
    accts = accounts.select_by_fund_id(ledger["fundId"], translate=False)

    __update_unused_accounts(accts, line_items)
    __update_unused_ledger(ledger)

    return 200, {}


def __update_unused_accounts(accounts_, line_items):
    """Check to see if line items still exist for old accounts"""
    account_lookup = {}
    for acct in accounts_:
        account_lookup[acct["account_id"]] = acct

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
    
            