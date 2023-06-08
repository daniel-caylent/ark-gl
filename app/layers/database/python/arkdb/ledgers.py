"""This module adapts specifc methos to access the Aurora MySQL database for ledgers"""

# pylint: disable=import-error; Lambda layer dependency
from database.ledger import (
    app_to_db,
    delete,
    select_by_fund,
    select_by_uuid,
    insert,
    update,
    select_by_client_id as __select_by_client_id,
    select_count_with_post_date,
)
from database.db_main import translate_to_app
# pylint: enable=import-error

from utils import DB_NAME, REGION_NAME, SECRET_NAME


def delete_by_id(uuid) -> None:
    delete(DB_NAME, uuid, REGION_NAME, SECRET_NAME)


def select_by_fund_id(fund_id):
    results = select_by_fund(DB_NAME, fund_id, REGION_NAME, SECRET_NAME)

    translated = [translate_to_app(app_to_db, result) for result in results]
    filtered = [
        {k: each[k] for k in each if not k.startswith("missing")} for each in translated
    ]
    return filtered


def select_by_id(uuid: str) -> dict:
    result = select_by_uuid(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    if result is None:
        return result

    translated = translate_to_app(app_to_db, result)
    filtered = {k: translated[k] for k in translated if not k.startswith("missing")}

    return filtered


def update_by_id(uuid: str, ledger: dict) -> None:
    update(DB_NAME, uuid, ledger, REGION_NAME, SECRET_NAME)


def select_by_client_id(uuid: str) -> dict:
    results = __select_by_client_id(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    translated = [translate_to_app(app_to_db, result) for result in results]
    filtered = [
        {k: each[k] for k in each if not k.startswith("missing")} for each in translated
    ]

    return filtered


def select_count_commited_ledgers() -> str:
    result = select_count_with_post_date(DB_NAME, REGION_NAME, SECRET_NAME)
    return result


def create_new(ledger: dict) -> str:
    result = insert(DB_NAME, ledger, REGION_NAME, SECRET_NAME)

    return result
