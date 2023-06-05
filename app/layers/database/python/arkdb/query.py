from .connection import get_db
from database.db_main import (
    execute_multiple_record_select,
    execute_single_record_select,
)


def run_query(query: str, multi=False) -> dict or list[dict]:
    conn = get_db()

    if multi is False:
        results = execute_single_record_select(conn, query)
    else:
        results = execute_multiple_record_select(conn, query)

    return results