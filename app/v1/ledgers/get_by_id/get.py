from arkdb import ledgers # pylint: disable=import-error
from shared import endpoint, validate_uuid # pylint: disable=import-error
from models import Ledger # pylint: disable=import-error


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

    ledger = Ledger(**result)

    return 200, {'data': ledger}
