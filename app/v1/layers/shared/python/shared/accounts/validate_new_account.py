from arkdb import accounts, account_attributes, funds
from models import AccountPost

def validate_new_account(account: dict) -> tuple[int, str, AccountPost]:
    
    # Check for missing details
    if account.get('fundId') is None:
        return 400, "No fund specified.", None
    if account.get('attributeId') is None:
        return 400, "No attribute specified.", None

    # validate the POST contents
    try:
        post = AccountPost(**account)
    except Exception as e:
        remove_str = "__init__() got an "
        error_str = str(e).strip(remove_str)

        return 400, error_str[0].upper() + error_str[1:], None

    # validate that the fund exists and client has access to it
    fund = funds.select_by_uuid(post.fundId)
    if fund is None:
        return 400, "Specified fund does not exist.", None

    # get accounts with the same name
    accts = accounts.select_by_fund_id(post.fundId)
    unique = validate_unique_account(post, accts)
    if unique is False:
        return 409, "Account number or name already exists in this fund.", None

    # validate the parent account exists
    if post.parentAccountId:
        parent = validate_parent_account(post, accts)
        if not parent:
            return 400, "Parent account does not exist in this fund.", None

    # validate the attribute exists
    attribute = account_attributes.select_by_id(post.attributeId)
    if attribute is None:
        return 400, "Specified account attribute does not exist.", None

    return 201, '', {'state': "UNUSED", **post.__dict__}


def validate_unique_account(account: AccountPost, existing_accounts):
    """Validate the incoming account has a unique name and number"""

    for acct in existing_accounts:
        if (acct['accountName'].lower() == account.accountName.lower()
                or acct['accountNo'] == account.accountNo):
            return False

    return True

def validate_parent_account(account: AccountPost, existing_accounts):
    """Validate the parent id supplied for this account exists"""
    for existing_account in existing_accounts:
        if account.parentAccountId == existing_account['accountId']:
            return True

    return False
