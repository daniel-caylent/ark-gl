"""This module provides the Aurora MySQL serverless capabilities for account attributes"""
from . import db_main
from . import connection


def __get_all_query(db: str) -> tuple:
    """
    This function creates the query that returns all account_attributes.

    db: string
    This parameter specifies the db name where the query will be executed

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """
        SELECT accatt.uuid as attributeId, accatt.account_type as accountType, accatt.detail_type as detailType
        FROM """
        + db
        + """.account_attribute accatt;"""
    )

    return (query, None)


def select_all(db: str, region_name: str, secret_name: str) -> list:
    """
    This function returns the record from the result of the "get all" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list of dicts containing all the account_attributes
    """

    params = __get_all_query(db)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record_list = db_main.execute_multiple_record_select(conn, params)

    return record_list


def __get_query_select_by_uuid(db: str, uuid: str) -> tuple:
    """
    This function creates the query that gets an account_attribute by uuid.

    db: string
    This parameter specifies the db name where the query will be executed

    uuid: string
    This parameter specifies the uuid that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = "SELECT * FROM " + db + ".account_attribute where uuid = %s;"

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
    A dict containing the account_attribute that matches with the upcoming uuid
    """
    params = __get_query_select_by_uuid(db, uuid)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_single_record_select(conn, params)

    return record


def get_id(db: str, uuid: str, region_name: str, secret_name: str) -> str:
    """
    This function returns the id from an account_attribute with a specified uuid.

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
    A string representing the id of that Account Attribute record with uuid equals to the input
    """
    record = select_by_uuid(db, uuid, region_name, secret_name)

    return record.get("id")
