import pymysql

from database.connection import get_connection
from . import utils


def get_db(**kwargs) -> pymysql.connect:

    conn = get_connection(
        utils.DB_NAME,
        utils.REGION_NAME,
        utils.SECRET_NAME,
        **kwargs
    )

    return conn