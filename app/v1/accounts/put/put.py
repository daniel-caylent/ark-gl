import json

from arkdb import accounts, account_attributes  # pylint: disable=import-error
from shared import (                            # pylint: disable=import-error
    endpoint,
    validate_uuid,
    update_dict
  )
from models import AccountPut                   # pylint: disable=import-error

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
    except Exception:
        return 400, {'detail': "Body does not contain valid data."}

    # verify account exists
    acct = accounts.select_by_id(account_id)
    if acct is None:
        return 404, {'detail': "No account found."}

    if acct['state'] != 'UNUSED':
        for key in body.keys():
            if key not in COMMITED_CHANGEABLE:
                return 400, {'detail': "Account cannot be modified."}

    # validate no other accounts exist with number or name
    accts = accounts.select_by_fund_id(acct['fundId'])
    unique = validate_unique_account(account_id, put, accts)
    if unique is False:
        return 409, {'detail': "Account number or name already exists in this fund."}
    
    # validate parent exists if part of this request
    if put.parentAccountId:
        parent = validate_parent_account(put, accts)
        if not parent:
            return 400, {'detail': "Parent account does not exist in this fund."}

    # if an attribute is part of this request, validate it exists
    if put.attributeId:
        attribute = account_attributes.select_by_id(put.attributeId)
        if not attribute:
            return 400, {'detail': "Account attribute does not exist."}

    # only keep fields present in the initial body, but replace
    # with type safe values from dataclass
    type_safe_body = update_dict(body, put.__dict__)
    accounts.update_by_id(account_id, type_safe_body)
    return 200, {}


def validate_unique_account(account_id: str, account: AccountPut, existing_accounts):
    """Validate the incoming account has a unique name and number"""

    for acct in existing_accounts:
        if acct['accountId'] == account_id:
            continue

        if account.accountName:
            if acct['accountName'].lower() == account.accountName.lower():
                return False

        if account.accountNo:
            if acct['accountNo'] == account.accountNo:
                return False

    return True

def validate_parent_account(account: AccountPut, existing_accounts):
    """Validate the parent id supplied for this account exists"""

    for existing_account in existing_accounts:
        if account.parentAccountId == existing_account['accountId']:
            return True

    return False
