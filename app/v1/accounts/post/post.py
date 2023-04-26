import json

from arkdb import accounts
from models import AccountPost
from shared import endpoint


@endpoint
def handler(event, context) -> tuple[int, dict]:
    try:
        body = json.loads(event['body'])
    except:
        return 400, {'detail': "Body does not contain valid json."}

    # check fund and attribute id to return specific messages
    if body.get('fundId') is None:
        return 400, {'detail': "No fund specified."}
    if body.get('attributeId') is None:
        return 400, {'detail': "No attribute specified."}

    # validate the POST body
    try:
        post = AccountPost(**body)
    except:
        return 400, {'detail': "Body does not contain valid data."}

    # get accounts with the same name
    accts = accounts.select_by_name(post.accountName)
    if len(accts) > 0:
        return 400, {'detail': "Account name already exists in this fund."}

    # try to insert the account
    try:
        result = accounts.create_new(post.__dict__)
    except Exception as e:
        return 400, {'detail': f"Failed to insert account due to: {str(e)}"}

    return 201, {'accountId': result}


def check_unique_account_name(fundId, name):
    # results = db.get_accounts_by_name(fundId, name)
    results = []

    return len(results) == 0
    
