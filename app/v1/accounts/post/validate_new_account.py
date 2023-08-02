"""Validations for Accounts POST"""

# pylint: disable=import-error; Lambda layer dependency
from arkdb import accounts, account_attributes
from models import AccountPost
from shared import dataclass_error_to_str

# pylint: enable=import-error


def validate_new_account(account: dict) -> tuple[int, str, AccountPost]:
    """Account validator"""

    # Check for missing details
    if account.get("attributeId") is None:
        return 400, "No attribute specified.", None

    # validate the POST contents
    try:
        post = AccountPost(**account)
    except Exception as e:
        return 400, dataclass_error_to_str(e), None

    # get accounts with the same name
    accts = accounts.select_by_fund_id(post.fundId)
    unique, reason = validate_unique_account(post, accts)
    if unique is False:
        return 409, reason, None

    # validate the parent account exists
    if post.parentAccountId:
        parent = validate_parent_account(post, accts)
        if not parent:
            return 400, "Parent account does not exist in this fund.", None

    if post.fsMappingId:
        if not validate_fs_account(post, accts):
            return 400, "fsMappingId does not relate to an existing account.", None

    # validate the attribute exists
    attribute = account_attributes.select_by_id(post.attributeId)
    if attribute is None:
        return 400, "Specified account attribute does not exist.", None

    return 201, "", {"state": "UNUSED", **post.__dict__}


def validate_unique_account(account: AccountPost, existing_accounts):
    """Validate the incoming account has a unique name and number"""

    for acct in existing_accounts:
        if acct["accountName"].lower() == account.accountName.lower():
            return (
                False,
                f"Account name already exists in this fund: {acct['accountName'].lower() }",
            )

        if acct["accountNo"] == account.accountNo:
            return (
                False,
                f"Account number already exists in this fund: {acct['accountNo']}",
            )

    return True, None


def validate_parent_account(account: AccountPost, existing_accounts):
    """Validate the parent id supplied for this account exists"""
    for existing_account in existing_accounts:
        if account.parentAccountId == existing_account["accountId"]:
            return True

    return False


def validate_fs_account(account: AccountPost, existing_accounts):
    """Validate the parent id supplied for this account exists"""
    for existing_account in existing_accounts:
        if account.fsMappingId == existing_account["accountId"]:
            return True

    return False
