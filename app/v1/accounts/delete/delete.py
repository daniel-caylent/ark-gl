from arkdb import accounts    # pylint: disable=import-error
from shared import endpoint   # pylint: disable=import-error
from models import Account    # pylint: disable=import-error

@endpoint
def handler(event, context) -> tuple[int, dict]:
    account_id = event['pathParameters'].get('accountId', None)
    if account_id is None:
        return 400, {'detail': "No account specified."}

    result = accounts.select_by_id(account_id)
    if result is None:
        return 404, {'detail': "No account found."}

    if result['state'] != 'UNUSED':
        return 400, {'detail': "Account cannot be deleted."}

    try:
        accounts.delete_by_id(account_id)
    except Exception as e:
        return 400, {'detail': f'Unable to delete due to: {str(e)}'}

    return 200, {}
