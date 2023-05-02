import json

from arkdb import accounts                  # pylint: disable=import-error
from shared import (                        # pylint: disable=import-error
    endpoint,
    validate_uuid
)

@endpoint
def handler(event, context) -> tuple[int, dict]:
    account_id = event['pathParameters'].get('accountId', None)
    if account_id is None:
        return 400, {'detail': "No account specified."}

    if not validate_uuid(account_id):
        return 400, {'detail': "Invalid UUID provided."}

    # verify account exists
    acct = accounts.select_by_id(account_id)
    if acct is None:
        return 404, {'detail': "No account found."}

    if acct['state'] == "ACTIVE":
        return 400, {'detail': "Account already commited."}

    accounts.update_by_id(account_id, {'state': "ACTIVE"})
    return 200, {}
