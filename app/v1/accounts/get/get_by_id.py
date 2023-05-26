from arkdb import accounts                    # pylint: disable=import-error
from shared import endpoint, validate_uuid    # pylint: disable=import-error
from models import Account                    # pylint: disable=import-error

@endpoint
def handler(event, context) -> tuple[int, dict]:
    if not event.get('pathParameters'):
        return 400, {'detail': "Missing path parameters"}
    
    account_id = event['pathParameters'].get('accountId', None)
    if account_id is None:
        return 400, {'detail': "No account specified."}

    if not validate_uuid(account_id):
        return 400, {'detail': "Invalid UUID provided."}

    result = accounts.select_by_id(account_id)
    if result is None:
        return 404, {'detail': "No account found."}

    account = Account(**result)

    return 200, {'data': account}
