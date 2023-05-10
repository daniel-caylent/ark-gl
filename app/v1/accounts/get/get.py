from shared import endpoint, validate_uuid  # pylint: disable=import-error
from arkdb import accounts, funds  # pylint: disable=import-error
from models import Account  # pylint: disable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]:
    if not event.get("queryStringParameters"):
        return 400, {"detail": "Missing query string parameters"}

    fund_id = event["queryStringParameters"].get("fundId", None)
    if fund_id is None:
        return 400, {"detail": "No fund specified."}

    if not validate_uuid(fund_id):
        return 400, {"detail": "Invalid UUID provided."}

    # validate that the fund exists and client has access to it
    fund = funds.select_by_uuid(fund_id)
    if fund is None:
        return 400, {'detail': "Specified fund does not exist."}

    results = accounts.select_by_fund_id(fund_id)
    accts = [Account(**account) for account in results]

    return 200, {"data": accts}
