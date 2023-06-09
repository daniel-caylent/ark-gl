"""This module adapts specifc methos to access the Aurora MySQL database for funds"""

# pylint: disable=import-error; Lambda layer dependency
from database.fund_entity import (
    select_by_uuid as select_by_uuid_,
)
from .utils import DB_NAME, REGION_NAME, SECRET_NAME
# pylint: enable=import-error

def select_by_uuid(uuid: str) -> list:
    """Select a fund by uuid"""
    result = select_by_uuid_(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    return result
