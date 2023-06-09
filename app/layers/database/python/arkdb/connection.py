"""This module provides the connection to the Aurora MySQL serverless database"""

import pymysql

from database.connection import (
    get_connection,
)  # pylint: disable=import-error; Lambda layer dependency

from .utils import DB_NAME, REGION_NAME, SECRET_NAME


def get_db(**kwargs) -> pymysql.connect:
    """Create a db connection from default values"""
    conn = get_connection(DB_NAME, REGION_NAME, SECRET_NAME, **kwargs)

    return conn
