"""This module provides the Aurora MySQL serverless capabilities for attachments"""

from . import db_main
from . import connection

app_to_db = {
    "documentId": "uuid",
    "documentMemo": "memo",
    "journal_entry_id": "journal_entry_id",
}


def get_insert_query(
    db: str,
    input_: dict,
    journal_entry_id: str,
) -> tuple:
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
        + """.attachment
            (uuid, journal_entry_id, memo)
        VALUES
            (%s, %s, %s);"""
    )

    translated_input = db_main.translate_to_db(app_to_db, input_)

    params = (
        translated_input.get("uuid"),
        journal_entry_id,
        translated_input.get("memo"),
    )

    return (query, params)


def get_update_query(db: str, id_: str, input_: dict) -> tuple:
    """
    This function creates the update query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id_: string
    This parameter specifies the uuid for identifying the attachment that will be updated

    input_: dictionary
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
        + """.attachment
        SET """
    )
    where_clause = "WHERE uuid = %s;"

    translated_input = db_main.translate_to_db(app_to_db, input_)

    if "uuid" in translated_input:
        del translated_input["uuid"]

    set_clause = ""
    params = ()
    for key in translated_input.keys():
        set_clause += str(key) + " = %s,\n"
        params += (translated_input.get(key),)

    size = len(set_clause)
    # Slice string to remove last 3 characters from string
    set_clause = set_clause[: size - 2]
    set_clause += "\n "

    params += (id_,)

    query = update_query + set_clause + where_clause

    return (query, params)


def __get_by_document_id_query(db: str, uuid: str) -> tuple:
    """
    This function creates the select by document_id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    uuid: string
    This parameter specifies the uuid that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = "SELECT * FROM " + db + ".attachment where uuid = %s;"

    params = (uuid,)

    return (query, params)


def select_by_document_id(
    db: str, uuid: str, region_name: str, secret_name: str
) -> dict:
    """
    This function returns the record from the result of the "select by document_id" query with its parameters.

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
    A dict containing the attachment that match with the upcoming uuid
    """
    params = __get_by_document_id_query(db, uuid)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_single_record_select(conn, params)

    return record


def __get_by_journal_query(db: str, journal_entry_id: str) -> tuple:
    """
    This function creates the select journal_entry_id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    journal_entry_id: string
    This parameter specifies the journal_entry_id that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = "SELECT * FROM " + db + ".attachment where journal_entry_id = %s;"

    params = (journal_entry_id,)

    return (query, params)


def select_by_journal(
    db: str, journal_entry_id: str, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select by journal" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    journal_entry_id: string
    This parameter specifies the journal_entry_id that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list of dicts containing the attachments that match with the upcoming journal_entry_id
    """
    params = __get_by_journal_query(db, journal_entry_id)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def get_delete_query(db: str, id_: str) -> tuple:
    """
    This function creates the delete query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id_: string
    This parameter specifies the uuid for the element to be deleted

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """
        DELETE FROM """
        + db
        + """.attachment
        WHERE uuid = %s;"""
    )

    params = (id_,)

    return (query, params)


def get_delete_by_journal_query(db: str, journal_entry_id: str) -> tuple:
    """
    This function creates the delete by journal_entry_id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    journal_entry_id: string
    This parameter specifies the journal_entry_id for the element/s to be deleted

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """
        DELETE FROM """
        + db
        + """.attachment
        WHERE journal_entry_id = %s;"""
    )

    params = (journal_entry_id,)

    return (query, params)


def __get_by_multiple_journals_query(db: str, journal_entry_ids: list) -> tuple:
    """
    This function creates the select by multiple journal_entry_id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    journal_entry_id: string
    This parameter specifies the journal_entry_id that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    format_strings = ",".join(["%s"] * len(journal_entry_ids))

    query = (
        """SELECT *
    FROM """
        + db
        + f".attachment where journal_entry_id IN ({format_strings});"
    )

    params = tuple(journal_entry_ids)

    return (query, params)


def select_by_multiple_journals(
    db: str, journal_entry_ids: list, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select by multiple journals" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    journal_entry_id: string
    This parameter specifies the journal_entry_ids that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A dict containing the attachments that match with the upcoming journal_entry_ids
    """
    params = __get_by_multiple_journals_query(db, journal_entry_ids)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def __get_by_uuid_journal_query(
    db: str, document_uuid: str, journal_entry_id: str
) -> tuple:
    """
    This function creates the select journal_entry_id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    document_uuid: string
    This parameter specifies the uuid that will be used for this query

    journal_entry_id: string
    This parameter specifies the journal_entry_id that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = "SELECT * FROM " + db + ".attachment where uuid = %s journal_entry_id = %s;"

    params = (document_uuid, journal_entry_id)

    return (query, params)


def select_by_uuid_journal(
    db: str,
    document_uuid: str,
    journal_entry_id: str,
    region_name: str,
    secret_name: str,
) -> dict:
    """
    This function returns the record from the result of the "select by journal" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    document_uuid: string
    This parameter specifies the uuid that will be used for this query

    journal_entry_id: string
    This parameter specifies the journal_entry_id that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list of dicts containing the attachments that match with the upcoming journal_entry_id
    """
    params = __get_by_uuid_journal_query(db, document_uuid, journal_entry_id)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_single_record_select(conn, params)

    return record
