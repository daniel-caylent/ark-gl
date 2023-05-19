from arkdb import ledgers    # pylint: disable=import-error
from shared import endpoint, validate_uuid   # pylint: disable=import-error

@endpoint
def handler(event, context) -> tuple[int, dict]:
    if not event.get('pathParameters'):
        return 400, {'detail': "Missing path parameters"}

    ledger_id = event['pathParameters'].get('ledgerId', None)
    if ledger_id is None:
        return 400, {'detail': "No ledger specified."}

    if not validate_uuid(ledger_id):
        return 400, {'detail': "Invalid UUID provided."}

    result = ledgers.select_by_id(ledger_id)
    if result is None:
        return 404, {'detail': "No ledger found."}

    if result['state'] == 'COMMITTED':
        return 400, {'detail': "COMMITTED ledger cannot be deleted."}

    try:
        ledgers.delete_by_id(ledger_id)
    except Exception as e:
        return 400, {'detail': f'Unable to delete. Ledger may have journal entries.'}

    return 200, {}
