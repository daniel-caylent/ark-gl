"""This module provides the Aurora MySQL serverless capabilities for the common methods for all entities"""
from pymysql import Connection, cursors


def translate_to_db(app_to_db: dict, input: dict) -> dict:
    """
    This function translates the input from app-format fields to db-format.

    app_to_db: dictionary
    This parameter specifies the dict that is used for translation
    that is particular to each entity

    input: dictionary
    This parameter contains all the parameters inside a dictionary that
    will be used for the translation

    return
    A dictionary containing the converted keys with the input values
    """
    return dict((app_to_db[key], value) for (key, value) in input.items())

def translate_to_app(app_to_db: dict, input:dict) -> dict:
    db_to_app = {v: k for k, v in app_to_db.items()}
    return dict((db_to_app.get(key,f'missing-{key}'), value) for (key, value) in input.items())

def translate_to_app(app_to_db: dict, input: dict) -> dict:
    """
    This function translates the input from db-format fields to app-format.

    app_to_db: dictionary
    This parameter specifies the dict that is used for translation
    that is particular to each entity

    input: dictionary
    This parameter contains all the parameters inside a dictionary that
    will be used for the translation

    return
    A dictionary containing the converted keys with the input values
    """
    results = None
    if input is not None:
        db_to_app = {v: k for k, v in app_to_db.items()}
        results = dict(
            (db_to_app.get(key, f"missing-{key}"), value)
            for (key, value) in input.items()
        )
    return results


def execute_dml(connection: Connection, query_list: list[tuple]) -> None:
    """
    This function executes a dml query/queries in the db.

    connection: Connection
    This parameter is a pymysql.Connection that specifies
    which endpoint and db the queries will impact

    query_list: list
    This parameter is a list of tuples that contains
    all queries to be executed with their parameters
    """
    cursor = connection.cursor()

    try:
        for item in query_list:
            query = item[0]
            data = item[1]
            cursor.execute(query, data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()

    return


def execute_single_record_select(connection: Connection, query_params: tuple) -> dict:
    """
    This function executes a select query in the db to get a single record.

    connection: Connection
    This parameter is a pymysql.Connection that specifies
    which endpoint and db the queries will impact

    query_params: tuple
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections

    return
    A dict with the single record returned
    """
    cursor = connection.cursor(cursors.DictCursor)

    try:
        query = query_params[0]
        data = query_params[1]
        cursor.execute(query, data)
        record = cursor.fetchone()
    except Exception as e:
        raise
    finally:
        cursor.close()
        connection.close()

    return record


def execute_multiple_record_select(
    connection: Connection, query_params: tuple
) -> list[dict]:
    """
    This function executes a select query in the db to get a list of records.

    connection: Connection
    This parameter is a pymysql.Connection that specifies
    which endpoint and db the queries will impact

    query_params: tuple
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections

    return
    A list of dicts with the returned records
    """
    cursor = connection.cursor(cursors.DictCursor)

    try:
        query = query_params[0]
        data = query_params[1]
        cursor.execute(query, data)
        record_list = cursor.fetchall()
    except Exception as e:
        raise
    finally:
        cursor.close()
        connection.close()

    return record_list


def get_new_uuid(connection: Connection) -> str:
    """
    This function generates and returns a new UUID in the db.

    connection: Connection
    This parameter is a pymysql.Connection that specifies
    which endpoint and db the queries will impact

    return
    A string with the generated UUID
    """
    params = ("SELECT UUID() as id;", None)

    # conn = connection.get_connection(db, region_name, secret_name, 'ro')

    record = execute_single_record_select(connection, params)

    return record.get("id")
