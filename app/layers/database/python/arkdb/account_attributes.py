from database.account_attribute import select_all as select_all_, select_by_uuid
from .utils import DB_NAME, REGION_NAME, SECRET_NAME


def select_all() -> list[dict]:
    results = select_all_(DB_NAME, REGION_NAME, SECRET_NAME)

    return results


def select_by_id(id) -> dict:
    results = select_by_uuid(DB_NAME, id, REGION_NAME, SECRET_NAME)

    return results
