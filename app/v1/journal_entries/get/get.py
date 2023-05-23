"""Journal entries get by ledgerId handler"""

from arkdb import journal_entries, ledgers  # pylint: disable=import-error
from shared import endpoint, validate_uuid  # pylint: disable=import-error, no-name-in-module
from models import JournalEntry

@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument
    """Get journal entries by ledgerId"""

    if not event.get("queryStringParameters"):
        return 400, {"detail": "Missing query string parameters"}

    ledger_id = event["queryStringParameters"].get("ledgerId", None)
    if not ledger_id:
        return 400, {"detail": "No ledger ID specified."}

    if not validate_uuid(ledger_id):
        return 400, {"detail": "Invalid ledger UUID provided."}

    # validate that the fund exists and client has access to it
    ledger = ledgers.select_by_id(ledger_id)
    if ledger is None:
        return 400, {"detail": "Specified ledger does not exist."}

    # get and format the ledgers
    results = journal_entries.select_by_ledger_id(ledger_id)

    if results:
        for journal_entry in results:
            journal_entry_id = journal_entry.pop("id")
            journal_entry["lineItems"] = journal_entries.get_line_items(journal_entry_id)
            journal_entry["attachments"] = journal_entries.get_attachments(journal_entry_id)

    journal_entries_ = [JournalEntry(**result) for result in results]
    
    return 200, {"data": journal_entries_}
