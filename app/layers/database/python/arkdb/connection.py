"""This module provides the connection to the Aurora MySQL serverless database"""

import pymysql

from database.connection import get_connection # pylint: disable=import-error; Lambda layer dependency

from . import utils

def get_db(**kwargs) -> pymysql.connect:
    """Create a db connection from default values"""
    conn = get_connection(utils.DB_NAME, utils.REGION_NAME, utils.SECRET_NAME, **kwargs)

    return conn
