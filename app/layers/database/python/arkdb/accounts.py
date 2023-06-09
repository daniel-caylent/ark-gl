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
)

from database.line_item import select_by_account_id as get_line_items_by_id

# pylint: enable=import-error

from .utils import (
    DB_NAME,
    REGION_NAME,
    SECRET_NAME,
    translate_result,
    translate_results,
)


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
