"""Shared validators for accounts PUT"""

# pylint: disable=import-error; Lambda layer dependency
from models import AccountPut

def validate_unique_account(account_id: str, account: AccountPut, existing_accounts):
    """Validate the incoming account has a unique name and number"""

    for acct in existing_accounts:
        if acct["accountId"] == account_id:
            continue

        if account.accountName:
            if acct["accountName"].lower() == account.accountName.lower():
                return False

        if account.accountNo:
            if acct["accountNo"] == account.accountNo:
                return False

    return True


def validate_parent_account(account: AccountPut, existing_accounts):
    """Validate the parent id supplied for this account exists"""

    for existing_account in existing_accounts:
        if account.parentAccountId == existing_account["accountId"]:
            return True

    return False


def validate_fs_account(account: AccountPut, existing_accounts):
    """Validate the parent id supplied for this account exists"""
    for existing_account in existing_accounts:
        if account.fsMappingId == existing_account["accountId"]:
            return True

    return False


def check_missing_fields(account_dict):
    """
    Check that the account information about to be updated does not input
    any null values for required fields
    """
    required = [
        "accountNo",
        "accountName",
        "fundId",
        "isTaxable",
        "attributeId",
        "isEntityRequired",
    ]

    keys = list(account_dict.keys())
    for field in required:
        if field in keys:
            value = account_dict[field]

            if value is None or value == "":
                return field

    return None
