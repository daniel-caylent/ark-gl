"""Module that defines a method to query to the Aurora MySQL serverless"""

# pylint: disable=import-error; Lambda layer dependency
from database.db_main import (
    execute_multiple_record_select,
    execute_single_record_select,
)
from .connection import get_db
# pylint: enable=import-error


def run_query(query: str, multi=False) -> dict or list[dict]:
    """Method to run a custom query to the mysql database"""
    conn = get_db()

    if multi is False:
        results = execute_single_record_select(conn, query)
    else:
        results = execute_multiple_record_select(conn, query)

    return results
