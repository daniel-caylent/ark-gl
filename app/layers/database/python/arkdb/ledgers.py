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
    commit,
    bulk_delete as __bulk_delete,
    select_by_fund_and_name as __select_by_fund_and_name,
    bulk_state as __bulk_state
)

# pylint: enable=import-error

from .utils import (
    DB_NAME,
    REGION_NAME,
    SECRET_NAME,
    translate_result,
    translate_results,
)


def delete_by_id(uuid) -> None:
    """Delete an existing ledger"""
    delete(DB_NAME, uuid, REGION_NAME, SECRET_NAME)


def select_by_fund_id(fund_id):
    """Select a list of ledgers by fund ID"""
    results = select_by_fund(DB_NAME, fund_id, REGION_NAME, SECRET_NAME)

    results = translate_results(results, app_to_db)
    return results


def select_by_fund_and_name(fund_id: str, name: str, translate=True) -> dict:
    """Select a ledger using a fund id and unique name"""
    result = __select_by_fund_and_name(DB_NAME, fund_id, name, REGION_NAME, SECRET_NAME)

    if translate:
        result = translate_result(result, app_to_db)

    return result

def select_by_id(uuid: str, translate=True) -> dict:
    """Select a ledger by UUID"""
    result = select_by_uuid(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    if translate:
        result = translate_result(result, app_to_db)

    return result

def update_by_id(uuid: str, ledger: dict) -> None:
    """Update a ledger by UUID"""
    update(DB_NAME, uuid, ledger, REGION_NAME, SECRET_NAME)


def select_by_client_id(uuid: str) -> dict:
    """Select a list of ledgers by client ID"""
    results = __select_by_client_id(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    results = translate_results(results, app_to_db)
    return results


def select_count_commited_ledgers() -> str:
    """Count committed ledgers"""
    result = select_count_with_post_date(DB_NAME, REGION_NAME, SECRET_NAME)
    return result


def create_new(ledger: dict) -> str:
    """Create a new ledger from dict"""
    result = insert(DB_NAME, ledger, REGION_NAME, SECRET_NAME)

    return result

def commit_by_id(ledger_uuid) -> None:
    """Commit an existing ledger"""
    commit(DB_NAME, ledger_uuid, REGION_NAME, SECRET_NAME)

def bulk_state(ledgers_list):
    """Update the state of multiple accounts from a list"""
    __bulk_state(DB_NAME, ledgers_list, REGION_NAME, SECRET_NAME)

def bulk_delete(ledgers_list):
    """Delete multiple ledgers from a list of UUIDs"""
    __bulk_delete(DB_NAME, ledgers_list, REGION_NAME, SECRET_NAME)

