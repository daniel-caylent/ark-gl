from database.account import (
    app_to_db,
    __get_select_by_fund_query,
    select_by_uuid,
    get_query_select_by_name,
    insert
)
from database.db_main import translate_to_app
from .query import run_query
from .utils import DB_NAME, REGION_NAME, SECRET_NAME

def select_by_fund_id(fund_id: int) -> list:
    query = __get_select_by_fund_query(DB_NAME, fund_id)
    results = run_query(query, multi=True)

    translated = [translate_to_app(app_to_db, result) for result in results]
    filtered = [{k: each[k] for k in each if not k.startswith('missing')} for each in translated]

    return filtered

def select_by_id(account_uuid: str) -> dict:
    query = select_by_uuid(DB_NAME, account_uuid, REGION_NAME, SECRET_NAME)
    result = run_query(query)

    if result is None:
        return result

    translated = translate_to_app(app_to_db, result)
    filtered = {k: translated[k] for k in translated if not k.startswith('missing')}

    return filtered

def create_new(account: dict) -> str:
    result = insert(DB_NAME, account, REGION_NAME, SECRET_NAME)

    return result
