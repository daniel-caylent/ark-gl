import json

from arkdb import accounts, funds
from models import AccountPost
from shared import endpoint


@endpoint
def handler(event, context) -> tuple[int, dict]:
    try:
        body = json.loads(event['body'])
    except:
        return 400, {'detail': "Body does not contain valid json."}

    # return specific messages for missing details
    if body.get('fundId') is None:
        return 400, {'detail': "No fund specified."}
    if body.get('attributeId') is None:
        return 400, {'detail': "No attribute specified."}

    # validate the POST body
    try:
        post = AccountPost(**body)
    except:
        return 400, {'detail': "Body does not contain valid data."}

    # validate that the fund exists and client has access to it
    fund = funds.select_by_uuid(post.fundId)
    if fund is None:
        return 400, {'detail': "Specified fund does not exist."}

    # get accounts with the same name
    accts = accounts.select_by_fund_id(post.fundId)
    unique = validate_unique_account(post, accts)
    if unique is False:
        return 409, {'detail': "Account number or name already exists in this fund."}

    # insert the new account
    try:
        result = accounts.create_new(post.__dict__)
    except Exception as e:
        return 400, {'detail': f"Failed to insert account due to: {str(e)}"}

    return 201, {'accountId': result}

def validate_unique_account(account: AccountPost, existing_accounts):
    for acct in existing_accounts:
        if acct['accountName'] == account.accountName or acct['accountNo'] == account.accountNo:
            return False
        
    return True
