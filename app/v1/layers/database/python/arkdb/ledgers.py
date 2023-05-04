from database.ledger import (
    app_to_db,
    select_by_fund,
    select_by_uuid
)
from database.db_main import translate_to_app

from .utils import DB_NAME, REGION_NAME, SECRET_NAME


def select_by_fund_id(fund_id):
    results = select_by_fund(DB_NAME, fund_id, REGION_NAME, SECRET_NAME)

    print(results)
    translated = [translate_to_app(app_to_db, result) for result in results]
    filtered = [{k: each[k] for k in each if not k.startswith('missing')} for each in translated]
    print(f'filtered: {filtered}')
    return filtered

def select_by_id(uuid: str) -> dict:
    result = select_by_uuid(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    if result is None:
        return result

    translated = translate_to_app(app_to_db, result)
    filtered = {k: translated[k] for k in translated if not k.startswith('missing')}

    return filtered
