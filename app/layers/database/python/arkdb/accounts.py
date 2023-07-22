"""This module adapts specifc methos to access the Aurora MySQL database for accounts"""

# pylint: disable=import-error; Lambda layer dependency
from database.account import (
    app_to_db,
    select_by_fund,
    select_by_uuid,
    select_count_with_post_date,
    insert,
    delete,
    update,
    commit,
    get_recursive_childs_by_uuids,
    get_recursive_parents_by_uuids,
    bulk_insert as __bulk_insert,
    bulk_update as __bulk_update,
    bulk_delete as __bulk_delete
)

from .utils import DB_NAME, REGION_NAME, SECRET_NAME

from database.line_item import (
    select_by_account_id as get_line_items_by_id,
    select_count_by_account_id
)

from .utils import (
    DB_NAME,
    REGION_NAME,
    SECRET_NAME,
    translate_result,
    translate_results,
)

# pylint: enable=import-error


def select_by_fund_id(fund_id: str, translate=True) -> list:
    """Select a list of accounts with a common fund ID"""
    results = select_by_fund(DB_NAME, fund_id, REGION_NAME, SECRET_NAME)

    if translate:
        results = translate_results(results, app_to_db)
    return results


def select_by_id(account_uuid: str, translate=True) -> dict:
    """Select a specific account by id"""
    result = select_by_uuid(DB_NAME, account_uuid, REGION_NAME, SECRET_NAME)

    if translate:
        result = translate_result(result, app_to_db)
    return result


def create_new(account: dict) -> str:
    """Create a new account from a dictionary"""
    result = insert(DB_NAME, account, REGION_NAME, SECRET_NAME)

    return result


def delete_by_id(account_uuid) -> None:
    """Delete an existing account"""
    delete(DB_NAME, account_uuid, REGION_NAME, SECRET_NAME)


def select_count_commited_accounts() -> str:
    """Count POSTED accounts"""
    result = select_count_with_post_date(DB_NAME, REGION_NAME, SECRET_NAME)
    return result


def update_by_id(id_: str, account: dict) -> None:
    """Update an account by id"""
    if "isDryRun" in account.keys():
        account.pop("isDryRun")

    update(DB_NAME, id_, account, REGION_NAME, SECRET_NAME)


def get_line_items(account_id):
    """Retrieve all line items for an account"""

    return get_line_items_by_id(DB_NAME, account_id, REGION_NAME, SECRET_NAME)

def get_line_items_count(account_id):
    """Retrieve the number of line items associated with an account"""
    return select_count_by_account_id(DB_NAME, account_id, REGION_NAME, SECRET_NAME)

def commit_by_id(account_uuid) -> None:
    """Commit an existing account"""
    commit(DB_NAME, account_uuid, REGION_NAME, SECRET_NAME)

def bulk_insert(accounts_list):
    """Insert multiple accounts from a list"""
    result = __bulk_insert(DB_NAME, accounts_list, REGION_NAME, SECRET_NAME)
    return result

def bulk_update(accounts_list):
    """Insert multiple accounts from a list"""
    result = __bulk_update(DB_NAME, accounts_list, REGION_NAME, SECRET_NAME)
    return result

def bulk_delete(accounts_list):
    """Delete multiple accounts from a list"""
    result = __bulk_delete(DB_NAME, accounts_list, REGION_NAME, SECRET_NAME)
    return result

def get_child_accounts_from_list(uuids, translate=True):
    results = get_recursive_childs_by_uuids(DB_NAME, uuids, REGION_NAME, SECRET_NAME)

    if translate:
        results = translate_results(results, app_to_db)
    return results

def get_parent_accounts_from_list(uuids, translate=True):
    results = get_recursive_parents_by_uuids(DB_NAME, uuids, REGION_NAME, SECRET_NAME)

    if translate:
        results = translate_results(results, app_to_db)
    return results