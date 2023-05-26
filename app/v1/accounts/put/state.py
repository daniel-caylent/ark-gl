import json

from arkdb import accounts                  # pylint: disable=import-error
from shared import (                        # pylint: disable=import-error
    endpoint,
    validate_uuid
)

VALID_STATES = ["COMMITTED"]

@endpoint
def handler(event, context) -> tuple[int, dict]:
    if not event.get('pathParameters'):
        return 400, {'detail': "Missing path parameters"}

    account_id = event['pathParameters'].get('accountId', None)
    if account_id is None:
        return 400, {'detail': "No account specified."}

    if not validate_uuid(account_id):
        return 400, {'detail': "Invalid UUID provided."}

    # validate the request body
    try:
        body = json.loads(event['body'])
    except Exception:
        return 400, {'detail': "Body does not contain valid json."}

    state = body.get('state')
    if not state:
        return 400, {'detail': "No state specified."}

    # verify account exists
    acct = accounts.select_by_id(account_id)
    if acct is None:
        return 404, {'detail': "No account found."}

    if acct['state'] == "COMMITTED":
        return 400, {'detail': "Account is already committed."}

    if state not in VALID_STATES:
        return 400, {'detail': "State is invalid."}

    # hard coding the state so there's no chance of tampering
    accounts.update_by_id(account_id, {'state': 'COMMITTED'})
    return 200, {}