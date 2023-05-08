import json

from arkdb import accounts, funds # pylint: disable=import-error
from shared import endpoint, validate_uuid # pylint: disable=import-error
from shared.accounts import validate_new_account, sort_accounts_for_insert # pylint: disable=import-error

@endpoint
def handler(event, context) -> tuple[int, dict]:
    """Handler for the accounts copy-to POST request
    
    event: dict
    POST event passed in from API gateway. The key 'body' should
    cary the POST request as a JSON string

    context: LambdaContext
    Context about the instance of the lambda function
    """
    destination_fund_id = event['pathParameters'].get('fundId', None)
    if destination_fund_id is None:
        return 400, {'detail': "No destination fund specified."}

    # validate the request body
    try:
        body = json.loads(event['body'])
    except:
        return 400, {'detail': "Body does not contain valid json."}

    # check fundId exists
    source_fund_id = body.get('fundId')
    if not source_fund_id:
        return 400, {'detail': "Source fund ID was not supplied."}

    # validate UUIDs for input source and destination
    valid_destination = validate_uuid(destination_fund_id)
    valid_source = validate_uuid(source_fund_id)
    if not valid_source and valid_destination:
        return 400, {'detail': "Invalid UUID for source or destination fund."}

    # check destination fund actually exists
    destination_exists = funds.select_by_uuid(destination_fund_id)
    if not destination_exists:
        return 404, {'detail': "Fund not found."}

    # check source fund actually exists
    source_exists = funds.select_by_uuid(source_fund_id)
    if not source_exists:
        return 400, {'detail': "Source fund does not exist."}

    # check source accounts exist
    source_accounts = accounts.select_by_fund_id(source_fund_id)
    if len(source_accounts) == 0:
        return 400, {'detail': "No accounts in source fund."}

    # check destination fund is empty
    destination_accounts = accounts.select_by_fund_id(destination_fund_id)
    if len(destination_accounts) > 0:
        return 409, {'detail': "Accounts already exist in destination fund."}

    # sort accounts for correct insertion order
    sorted_accounts = sort_accounts_for_insert(source_accounts)

    # insert accounts one at a time, retaining UUIDs for child
    # accounts to lookup
    uuid_lookup = {}
    for acct in sorted_accounts:
        accountId = acct.pop('accountId')
        acct.pop('state')

        acct['fundId'] = destination_fund_id

        if acct['parentAccountId'] in uuid_lookup.keys():
            acct['parentAccountId'] = uuid_lookup[acct['parentAccountId']]

        code, detail, post = validate_new_account(acct)

        if code != 201:
            return code, {'detail': detail}
        # insert the new account and retain accountId mapping
        uuid_lookup[accountId] = accounts.create_new(post)

    return code, {'accountIds': list(uuid_lookup.values())}
