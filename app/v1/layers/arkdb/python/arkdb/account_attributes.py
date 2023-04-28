from database.account_attribute import get_all, select_by_uuid
from .query import run_query
from .utils import DB_NAME, REGION_NAME, SECRET_NAME


def select_all() -> list[dict]:
    results = get_all(DB_NAME, REGION_NAME, SECRET_NAME)

    return results

def select_by_id(id) -> dict:
    results = select_by_uuid(DB_NAME, id, REGION_NAME, SECRET_NAME)

    return results

