import json

from arkdb import accounts                  # pylint: disable=import-error
from shared import endpoint, validate_uuid  # pylint: disable=import-error
from models import AccountPut               # pylint: disable=import-error

COMMITED_CHANGEABLE = ['fsName', 'fsMappingId']

@endpoint
def handler(event, context) -> tuple[int, dict]:
    account_id = event['pathParameters'].get('accountId', None)
    if account_id is None:
        return 400, {'detail': "No account specified."}

    if not validate_uuid(account_id):
        return 400, {'detail': "Invalid UUID provided."}

    # validate the request body
    try:
        body = json.loads(event['body'])
    except:
        return 400, {'detail': "Body does not contain valid json."}

    if len(body.keys()) == 0:
        return 400, {'detail': "Body does not contain content."}

    # validate the PUT contents
    try:
        put = AccountPut(**body)
    except:
        return 400, {'detail': "Body does not contain valid data."}

    # verify account exists
    result = accounts.select_by_id(account_id)
    if result is None:
        return 404, {'detail': "No account found."}

    if result['state'] != 'UNUSED':
        for key in body.keys():
            if key not in COMMITED_CHANGEABLE:
                return 400, {'detail': "Account cannot be modified."}

    try:
        accounts.update_by_id(account_id, put.__dict__)
    except Exception as e:
        return 400, {'detail': f'Unable to update account due to: {str(e)}'}

    return 200, {}
