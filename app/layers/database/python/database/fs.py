"""This module provides the Aurora MySQL serverless capabilities for FS entities"""

from . import db_main
from . import connection


def get_insert_query(db: str, input: dict) -> tuple:
    """
    This function creates the insert query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    input: dictionary
    This parameter contains all the parameters inside a dictionary that
    will be used for the query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """
        INSERT INTO """
        + db
        + """.FS
            (fs_mapping_id, fs_name)
        VALUES
            (%s, %s);"""
    )

    params = (
        input.get("fs_mapping_id"),
        input.get("fs_name"),
    )

    return (query, params)


def get_update_query(db: str, fs_mapping_id: str, input: dict) -> tuple:
    """
    This function creates the update query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    fs_mapping_id: string
    This parameter specifies the fs_mapping_id for identifying the FS row
    that will be updated

    input: dictionary
    This parameter contains all the parameters inside a dictionary that
    will be used for the query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    update_query = (
        """
        UPDATE """
        + db
        + """.FS
        SET """
    )
    where_clause = "WHERE fs_mapping_id = %s;"

    set_clause = ""
    params = ()
    for key in input.keys():
        set_clause += str(key) + " = %s,\n"
        params += (input.get(key),)

    size = len(set_clause)
    # Slice string to remove last 3 characters from string
    set_clause = set_clause[: size - 2]
    set_clause += "\n "

    params += (fs_mapping_id,)

    query = update_query + set_clause + where_clause

    return (query, params)


def get_delete_query(db: str, fs_mapping_id: str) -> tuple:
    """
    This function creates the delete query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    fs_mapping_id: string
    This parameter specifies the fs_mapping_id for the element to be deleted

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """
        DELETE FROM """
        + db
        + """.FS
        WHERE fs_mapping_id = %s;"""
    )

    params = (fs_mapping_id,)

    return (query, params)


def __get_select_by_fs_mapping_id_query(db: str, fs_mapping_id: str) -> tuple:
    """
    This function creates the select by uuid query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    fs_mapping_id: string
    This parameter specifies the uuid that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """
        SELECT *
        FROM """
        + db
        + """.FS
        where fs_mapping_id = %s;"""
    )

    params = (fs_mapping_id,)

    return (query, params)


def select_by_fs_mapping_id(
    db: str, fs_mapping_id: str, region_name: str, secret_name: str
) -> dict:
    """
    This function returns the record from the result of the "select by fs_mapping_id" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    fs_mapping_id: string
    This parameter specifies the uuid that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A dict containing the FS entity that matches with the upcoming uuid
    """
    params = __get_select_by_fs_mapping_id_query(db, fs_mapping_id)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_single_record_select(conn, params)

    return record
