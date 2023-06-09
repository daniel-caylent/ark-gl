"""This module provides the Aurora MySQL serverless capabilities for fund entities"""

from . import db_main
from . import connection


def __get_select_by_uuid_query(db: str, uuid: str) -> tuple:
    """
    This function creates the select by uuid query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    uuid: string
    This parameter specifies the uuid that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = "SELECT * FROM " + db + ".fund_entity where uuid = %s;"

    params = (uuid,)

    return (query, params)


def select_by_uuid(db: str, uuid: str, region_name: str, secret_name: str) -> dict:
    """
    This function returns the record from the result of the "select by uuid" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    uuid: string
    This parameter specifies the uuid that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A dict containing the fund entity that matches with the upcoming uuid
    """
    params = __get_select_by_uuid_query(db, uuid)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_single_record_select(conn, params)

    return record


def get_id(db: str, uuid: str, region_name: str, secret_name: str) -> str:
    """
    This function returns the id from a fund entity with a specified uuid.

    db: string
    This parameter specifies the db name where the query will be executed

    uuid: string
    This parameter specifies the uuid that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A string representing the id of that Fund Entity record with uuid equals to the input
    """
    record = select_by_uuid(db, uuid, region_name, secret_name)

    return record.get("id")


def get_insert_query(db: str, input: dict) -> tuple:
    """
    This function creates the insert query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    input: dictionary
    This parameter contains all the parameters inside a dictionary that
    will be used for the query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """
        INSERT INTO """
        + db
        + """.fund_entity
            (uuid, client_id, fund_id)
        VALUES
            (%s, %s, %s);"""
    )

    params = (
        input.get("fund_entity_id"),
        input.get("client_id"),
        input.get("fund_entity_id"),
    )

    return (query, params)


def get_update_query(db: str, fund_entity_id: str, input: dict) -> tuple:
    """
    This function creates the update query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    fund_entity_id: string
    This parameter specifies the fund_entity_id for identifying the FS row
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
        + """.fund_entity
        SET """
    )
    where_clause = "WHERE uuid = %s;"

    set_clause = ""
    params = ()
    for key in input.keys():
        set_clause += str(key) + " = %s,\n"
        params += (input.get(key),)

    size = len(set_clause)
    # Slice string to remove last 3 characters from string
    set_clause = set_clause[: size - 2]
    set_clause += "\n "

    params += (fund_entity_id,)

    query = update_query + set_clause + where_clause

    return (query, params)


def get_delete_query(db: str, fund_entity_id: str) -> tuple:
    """
    This function creates the delete query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    fund_entity_id: string
    This parameter specifies the fund_entity_id for the element to be deleted

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """
        DELETE FROM """
        + db
        + """.fund_entity
        WHERE uuid = %s;"""
    )

    params = (fund_entity_id,)

    return (query, params)
