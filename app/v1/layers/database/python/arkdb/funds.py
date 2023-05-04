from database.fund_entity import select_by_uuid as select_by_uuid_
from .utils import DB_NAME, REGION_NAME, SECRET_NAME


def select_by_uuid(uuid: str) -> list:
    result = select_by_uuid_(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    return result
