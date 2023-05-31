import json

from arkdb import journal_entries                  # pylint: disable=import-error
from shared import (                        # pylint: disable=import-error
    endpoint,
    validate_uuid
)

VALID_STATES = ["COMMITTED"]

@endpoint
def handler(event, context) -> tuple[int, dict]:
    if not event.get('pathParameters'):
        return 400, {'detail': "Missing path parameters"}

    journal_entry_id = event['pathParameters'].get('journalEntryId', None)
    if journal_entry_id is None:
        return 400, {'detail': "No journal_entry specified."}

    if not validate_uuid(journal_entry_id):
        return 400, {'detail': "Invalid UUID provided."}

    # validate the request body
    try:
        body = json.loads(event['body'])
    except Exception:
        return 400, {'detail': "Body does not contain valid json."}

    state = body.get('state')
    if not state:
        return 400, {'detail': "No state specified."}

    # verify journal_entry exists
    acct = journal_entries.select_by_id(journal_entry_id)
    if acct is None:
        return 404, {'detail': "No journal entry found."}

    if acct['state'] == "COMMITTED":
        return 400, {'detail': "Journal entry is already committed."}

    if state not in VALID_STATES:
        return 400, {'detail': "State is invalid."}

    # hard coding the state so there's no chance of tampering
    journal_entries.update_by_id(journal_entry_id, {'state': 'COMMITTED'})
    return 200, {}
