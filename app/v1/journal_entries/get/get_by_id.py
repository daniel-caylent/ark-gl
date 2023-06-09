"""Lambda that will perform the GET for JournalEntries searching by Id"""

# pylint: disable=import-error; Lambda layer dependency
from arkdb import journal_entries
from shared import (
    endpoint,
    validate_uuid,
)
from models import JournalEntry
# pylint: enable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]:  # pylint: disable=unused-argument; Required lambda parameters
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
    line_items = journal_entries.get_line_items(journal_entry_id)
    attachments = journal_entries.get_attachments(journal_entry_id)

    for line_item in line_items:
        line_item.pop("journal_entry_id")
    for attachment in attachments:
        attachment.pop("journal_entry_id")

    journal_entry["lineItems"] = line_items
    journal_entry["attachments"] = attachments

    return 200, {"data": JournalEntry(**journal_entry)}
