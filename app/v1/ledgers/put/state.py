import json

from arkdb import ledgers                  # pylint: disable=import-error
from shared import (                        # pylint: disable=import-error
    endpoint,
    validate_uuid
)

VALID_STATES = ["POSTED"]

@endpoint
def handler(event, context) -> tuple[int, dict]:
    if not event.get('pathParameters'):
        return 400, {'detail': "Missing path parameters"}

    ledger_id = event['pathParameters'].get('ledgerId', None)
    if ledger_id is None:
        return 400, {'detail': "No ledger specified."}

    if not validate_uuid(ledger_id):
        return 400, {'detail': "Invalid UUID provided."}

    # validate the request body
    try:
        body = json.loads(event['body'])
    except:
        return 400, {'detail': "Body does not contain valid json."}

    state = body.get('state')
    if not state:
        return 400, {'detail': "No state specified."}

    # verify ledger exists
    ledger = ledgers.select_by_id(ledger_id)
    if ledger is None:
        return 404, {'detail': "No ledger found."}

    if ledger['state'] == "POSTED":
        return 400, {'detail': "Ledger is already POSTED."}
    
    if state not in VALID_STATES:
        return 400, {'detail': "State is invalid."}
    
    # hard coding the state so there's no chance of tampering
    ledgers.update_by_id(ledger_id, {'state': 'POSTED'})
    return 200, {}
