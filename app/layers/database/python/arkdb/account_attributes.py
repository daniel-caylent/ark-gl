"""This module adapts specifc methos to access the Aurora MySQL database for account attributes"""

from database.account_attribute import select_all as select_all_, select_by_uuid # pylint: disable=import-error; Lambda layer dependency
from .utils import DB_NAME, REGION_NAME, SECRET_NAME


def select_all() -> list[dict]:
    """Select all account attributes"""
    results = select_all_(DB_NAME, REGION_NAME, SECRET_NAME)

    return results


def select_by_id(id_) -> dict:
    """Select a specific account attribute by ID"""
    results = select_by_uuid(DB_NAME, id_, REGION_NAME, SECRET_NAME)

    return results
