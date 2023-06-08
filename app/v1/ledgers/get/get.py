"""Lambda that will perform GET requests for Ledgers"""

# pylint: disable=import-error; Lambda layer dependency
from shared import endpoint, validate_uuid
from arkdb import ledgers, funds
from models import Ledger
# pylint: enable=import-error

@endpoint
def handler(event, context) -> tuple[int, dict]:
    """Handler for ledgers GET request

    event: dict
    POST event passed in from API gateway. The key 'body' should
    cary the POST request as a JSON string

    context: LambdaContext
    Context about the instance of the lambda function
    """

    if not event.get("queryStringParameters"):
        return 400, {"detail": "Missing query string parameters"}

    client_id = event["queryStringParameters"].get("clientId", None)
    fund_id = event["queryStringParameters"].get("fundId", None)

    if client_id is None and fund_id is None:
        return 400, {"detail": "No client or fund ID specified."}

    if fund_id:
        if not validate_uuid(fund_id):
            return 400, {"detail": "Invalid fund UUID provided."}
        # validate that the fund exists and client has access to it
        fund = funds.select_by_uuid(fund_id)
        if fund is None:
            return 400, {"detail": "Specified fund does not exist."}

        # get and format the ledgers
        results = ledgers.select_by_fund_id(fund_id)
    else:
        if not validate_uuid(client_id):
            return 400, {"detail": "Invalid client UUID provided."}

        results = ledgers.select_by_client_id(client_id)

    ledgers_ = []
    if results:
        ledgers_ = [Ledger(**ledger) for ledger in results]
    return 200, {"data": ledgers_}
