"""Lambda that will perform the PUT for JournalEntries / state"""
import json

# pylint: disable=import-error; Lambda layer dependency
from arkdb import journal_entries
from shared import (
    endpoint,
    validate_uuid,
)
# pylint: enable=import-error


VALID_STATES = ["POSTED"]


@endpoint
def handler(event, context) -> tuple[int, dict]:  # pylint: disable=unused-argument; Required lambda parameters
    if not event.get("pathParameters"):
        return 400, {"detail": "Missing path parameters"}

    journal_entry_id = event["pathParameters"].get("journalEntryId", None)
    if journal_entry_id is None:
        return 400, {"detail": "No journal_entry specified."}

    if not validate_uuid(journal_entry_id):
        return 400, {"detail": "Invalid UUID provided."}

    # validate the request body
    try:
        body = json.loads(event["body"])
    except Exception:
        return 400, {"detail": "Body does not contain valid json."}

    state = body.get("state")
    if not state:
        return 400, {"detail": "No state specified."}

    # verify journal_entry exists
    journal_entry = journal_entries.select_by_id(journal_entry_id, translate=False)
    if journal_entry is None:
        return 404, {"detail": "No journal entry found."}

    original_state = journal_entry['state']
    if original_state == "POSTED":
        return 400, {'detail': "Journal entry is already POSTED."}

    if state not in VALID_STATES:
        return 400, {"detail": "State is invalid."}

    try:
        journal_entries.commit_by_id(journal_entry_id)
    except Exception as e:
        return 500, {"detail": f"An error occurred when posting to QLDB: {str(e)}"}

    return 200, {}
