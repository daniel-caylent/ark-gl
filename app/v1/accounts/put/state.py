"""Lambda that will perform PUT requests for Accounts / state"""
from datetime import datetime
import json

# pylint: disable=import-error; Lambda layer dependency
from arkdb import accounts
import ark_qldb
from shared import endpoint, validate_uuid, dataclass_encoder
# pylint: enable=import-error

VALID_STATES = ["POSTED"]


@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters
    if not event.get("pathParameters"):
        return 400, {"detail": "Missing path parameters"}

    account_id = event["pathParameters"].get("accountId", None)
    if account_id is None:
        return 400, {"detail": "No account specified."}

    if not validate_uuid(account_id):
        return 400, {"detail": "Invalid UUID provided."}

    # validate the request body
    try:
        body = json.loads(event["body"])
    except Exception:
        return 400, {"detail": "Body does not contain valid json."}

    state = body.get("state")
    if not state:
        return 400, {"detail": "No state specified."}

    # verify account exists
    acct = accounts.select_by_id(account_id)
    if acct is None:
        return 404, {"detail": "No account found."}

    original_state = acct['state']
    if original_state == "POSTED":
        return 400, {'detail': "Account is already POSTED."}

    if state not in VALID_STATES:
        return 400, {"detail": "State is invalid."}

    # hard coding the state so there's no chance of tampering
    accounts.update_by_id(account_id, {'state': 'POSTED', 'postDate': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    account = accounts.select_by_id(account_id, translate=False)
    try:
        ark_qldb.post("account", dataclass_encoder.encode(account))
    except Exception as e:
        accounts.update_by_id(account_id, {'state': original_state, 'postDate': None})
        return 500, {"detail": f"An error occurred when posting to QLDB: {str(e)}"}

    return 200, {}
