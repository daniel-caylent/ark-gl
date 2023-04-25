from database import account_attribute as db_acct_attr
from .query import run_query
from .utils import DB_NAME


def get_all():
    query = db_acct_attr.get_all(DB_NAME)
    results = run_query(query, multi=True)

    return results
