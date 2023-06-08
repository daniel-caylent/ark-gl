"""Lambda that will perform GET requests for Ledgers searching by Id"""

# pylint: disable=import-error; Lambda layer dependency
from arkdb import ledgers
from shared import endpoint, validate_uuid
from models import Ledger
# pylint: enable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]:
    """Handler for ledgers GET by id request

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

    result = ledgers.select_by_id(ledger_id)
    if result is None:
        return 404, {"detail": "No ledger found."}

    ledger = Ledger(**result)

    return 200, {"data": ledger}
