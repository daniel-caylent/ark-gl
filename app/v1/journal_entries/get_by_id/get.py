"""Journal entries get-by-id"""

from arkdb import journal_entries  # pylint: disable=import-error
from shared import endpoint, validate_uuid  # pylint: disable=import-error, no-name-in-module


@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument
    """Journal Entried get-by-id handler"""

    if not event.get("pathParameters"):
        return 400, {"detail": "Missing path parameters"}

    journal_entry_uuid = event["pathParameters"].get("journalEntryId", None)
    if journal_entry_uuid is None:
        return 400, {"detail": "No journal entry specified."}

    if not validate_uuid(journal_entry_uuid):
        return 400, {"detail": "Invalid UUID provided."}

    journal_entry = journal_entries.select_by_id(journal_entry_uuid)
    if journal_entry is None:
        return 404, {"detail": "No journal entry found."}

    journal_entry_id = journal_entry.pop("id")
    journal_entry["lineItems"] = journal_entries.get_line_items(journal_entry_id)

    return 200, {"data": journal_entry}
