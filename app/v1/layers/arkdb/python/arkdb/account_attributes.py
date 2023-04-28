from database.account_attribute import get_all, get_query_select_by_uuid
from .query import run_query
from .utils import DB_NAME


def select_all() -> list[dict]:
    query = get_all(DB_NAME)
    results = run_query(query, multi=True)

    return results

def get_by_id(id) -> dict:
    query = get_query_select_by_uuid(DB_NAME, id)
    results = run_query(query)

    return results

