from arkdb import journal_entries    # pylint: disable=import-error
from shared import endpoint, validate_uuid   # pylint: disable=import-error

@endpoint
def handler(event, context) -> tuple[int, dict]:
    if not event.get('pathParameters'):
        return 400, {'detail': "Missing path parameters"}

    journal_entry_id = event['pathParameters'].get('journalEntryId', None)
    if journal_entry_id is None:
        return 400, {'detail': "No journal entry specified."}

    if not validate_uuid(journal_entry_id):
        return 400, {'detail': "Invalid UUID provided."}

    result = journal_entries.select_by_id(journal_entry_id)
    if result is None:
        return 404, {'detail': "No journal entry found."}

    if result['state'] == 'COMMITTED':
        return 400, {'detail': "COMMITTED journal entry cannot be deleted."}

    try:
        journal_entries.delete_by_id(journal_entry_id)
    except Exception as e:
        return 400, {'detail': f'Unable to delete: {str(e)}'}

    return 200, {}
