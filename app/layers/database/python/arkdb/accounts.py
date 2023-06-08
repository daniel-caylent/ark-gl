"""This module adapts specifc methos to access the Aurora MySQL database for accounts"""

from database.account import (
    app_to_db,
    select_by_fund,
    select_by_uuid,
    select_count_with_post_date,
    insert,
    delete,
    update,
)
from database.db_main import translate_to_app
from .utils import DB_NAME, REGION_NAME, SECRET_NAME


def select_by_fund_id(fund_id: str) -> list:
    """Select a list of accounts with a common fund ID"""
    results = select_by_fund(DB_NAME, fund_id, REGION_NAME, SECRET_NAME)

    translated = [translate_to_app(app_to_db, result) for result in results]
    filtered = [
        {k: each[k] for k in each if not k.startswith("missing")} for each in translated
    ]

    return filtered


def select_by_id(account_uuid: str, translate=True) -> dict:
    """Select a specific account by id"""
    result = select_by_uuid(DB_NAME, account_uuid, REGION_NAME, SECRET_NAME)

    if result is None:
        return result

    if translate:
        translated = translate_to_app(app_to_db, result)
        filtered = {k: translated[k] for k in translated if not k.startswith("missing")}
        return filtered

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


def update_by_id(id: str, account: dict) -> None:
    """Update an account by id"""
    if "isDryRun" in account.keys():
        account.pop("isDryRun")

    update(DB_NAME, id, account, REGION_NAME, SECRET_NAME)
