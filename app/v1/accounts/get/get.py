from shared import endpoint
from arkdb import accounts
from models import Account

@endpoint
def handler(event, context) -> tuple[int, dict]:
    fund_id = event['queryStringParameters'].get('fundId', None)
    if fund_id is None:
        return 400, {'detail': "No fund specified."}

    results = accounts.select_by_fund_id(fund_id)
    accts = [Account(**account) for account in results]

    return 200, {'data': accts}
