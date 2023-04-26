from database.account_attribute import get_all
from .query import run_query
from .utils import DB_NAME


def select_all() -> list[dict]:
    query = get_all(DB_NAME)
    results = run_query(query, multi=True)

    return results
