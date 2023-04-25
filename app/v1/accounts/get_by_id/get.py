
from arkdb import accounts
from shared import endpoint
from models import Account

@endpoint
def handler(event, context) -> tuple[int, dict]:
    account_id = event['pathParameters'].get('accountId', None)
    if account_id is None:
        return 400, {'detail': "No account specified."}

    result = accounts.select_by_id(account_id)
    if result is None:
        return 400, {'detail': "No account found."}

    account = Account(**result)

    return 200, {'data': account}
