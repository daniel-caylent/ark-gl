from shared import endpoint, validate_uuid  # pylint: disable=import-error
from arkdb import ledgers, funds  # pylint: disable=import-error
from models import Ledger


@endpoint
def handler(event, context) -> tuple[int, dict]:
    fund_id = event["queryStringParameters"].get("fundId", None)
    if fund_id is None:
        return 400, {"detail": "No fund specified."}

    if not validate_uuid(fund_id):
        return 400, {"detail": "Invalid UUID provided."}

    # validate that the fund exists and client has access to it
    fund = funds.select_by_uuid(fund_id)
    if fund is None:
        return 400, {'detail': "Specified fund does not exist."}

    # get and format the ledgers
    results = ledgers.select_by_fund_id(fund_id)
    ledgers_ = [Ledger(**ledger) for ledger in results]

    return 200, {"data": ledgers_}
