"""Lambda that will perform Ledgers / state"""
import json

# pylint: disable=import-error; Lambda layer dependency
from arkdb import ledgers
from shared import (
    endpoint,
    validate_uuid,
)

# pylint: enable=import-error


VALID_STATES = ["POSTED"]


@endpoint
def handler(
    event, context
) -> tuple[int, dict]:  # pylint: disable=unused-argument; Required lambda parameters
    """Handler for ledgers PUT state request

    event: dict
    POST event passed in from API gateway. The key 'body' should
    cary the POST request as a JSON string

    context: LambdaContext
    Context about the instance of the lambda function
    """

    if not event.get("pathParameters"):
        return 400, {"detail": "Missing path parameters"}

    ledger_id = event["pathParameters"].get("ledgerId", None)
    if ledger_id is None:
        return 400, {"detail": "No ledger specified."}

    if not validate_uuid(ledger_id):
        return 400, {"detail": "Invalid UUID provided."}

    # validate the request body
    try:
        body = json.loads(event["body"])
    except Exception:
        return 400, {"detail": "Body does not contain valid json."}

    state = body.get("state")
    if not state:
        return 400, {"detail": "No state specified."}

    # verify ledger exists
    ledger = ledgers.select_by_id(ledger_id)
    if ledger is None:
        return 404, {"detail": "No ledger found."}

    original_state = ledger["state"]
    if original_state == "POSTED":
        return 400, {"detail": "Ledger is already POSTED."}

    if state not in VALID_STATES:
        return 400, {"detail": "State is invalid."}

    try:
        ledgers.commit_by_id(ledger_id)
    except Exception as e:
        return 500, {"detail": f"An error occurred when posting to QLDB: {str(e)}"}

    return 200, {}
