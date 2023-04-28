import json

from arkdb import accounts, funds, account_attributes
from models import AccountPost
from shared import endpoint


@endpoint
def handler(event, context) -> tuple[int, dict]:
    # validate the request body
    try:
        body = json.loads(event['body'])
    except:
        return 400, {'detail': "Body does not contain valid json."}

    # Check for missing details
    if body.get('fundId') is None:
        return 400, {'detail': "No fund specified."}
    if body.get('attributeId') is None:
        return 400, {'detail': "No attribute specified."}

    # validate the POST contents
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

    # validate the parent account exists
    if post.parentAccountId:
        parent = validate_parent_account(post, accts)
        if parent is False:
            return 400, {'detail': "Parent account does not exist in this fund."}

    # validate the attribute exists
    attribute = account_attributes.select_by_id(post.attributeId)
    if attribute is None:
        return 400, {'detail': "Specified account attribute does not exist."}

    # insert the new account
    try:
        result = accounts.create_new(post.__dict__)
    except Exception as e:
        return 400, {'detail': f"Failed to insert account due to: {str(e)}"}

    return 201, {'accountId': result}


def validate_unique_account(account: AccountPost, existing_accounts):
    """Validate the incoming account has a unique name and number"""

    for acct in existing_accounts:
        if acct['accountName'].lower() == account.accountName.lower() or acct['accountNo'] == account.accountNo:
            return False
        
    return True

def validate_parent_account(account: AccountPost, existing_accounts):
    """Validate the parent id supplied for this account exists"""

    for existing_account in existing_accounts:
        if account.parentAccountId == existing_account['accountId']:
            return True

    return False
