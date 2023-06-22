"""This module provides the Aurora MySQL serverless capabilities for line items"""

from . import db_main
from . import connection
from . import account

app_to_db = {
    "lineItemNo": "line_number",
    "accountId": "account_id",
    "accountNo": "account_no",
    "accountName": "account_name",
    "amount": "amount",
    "memo": "memo",
    "type": "posting_type",
    "entityId": "entity_id",
    "journal_entry_id": "journal_entry_id",
}


def get_insert_query(
    db: str,
    parameters: dict,
    journal_entry_id: str,
    line_number: str,
    posting_type: str,
    region_name: str,
    secret_name: str,
) -> tuple:
    """
    This function creates the insert query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    parameters: dictionary
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
        + """.line_item
            (uuid, account_id, journal_entry_id, line_number, memo, posting_type, amount, entity_id)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s);"""
    )

    translated_input = db_main.translate_to_db(app_to_db, parameters)

    account_uuid = translated_input.get("account_id")
    account_id = account.get_id_by_uuid(db, account_uuid, region_name, secret_name)

    # Getting new uuid from the db to return it in insertion
    ro_conn = connection.get_connection(db, region_name, secret_name, "ro")
    uuid = db_main.get_new_uuid(ro_conn)

    params = (
        uuid,
        account_id,
        journal_entry_id,
        line_number,
        translated_input.get("memo"),
        posting_type,
        translated_input.get("amount"),
        translated_input.get("entity_id"),
    )

    return (query, params)


def get_update_query(db: str, id_: str, parameters: dict) -> tuple:
    """
    This function creates the update query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id: string
    This parameter specifies the uuid for identifying the line item
    that will be updated

    parameters: dictionary
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
        + """.line_item
        SET """
    )
    where_clause = "WHERE uuid = %s;"

    translated_input = db_main.translate_to_db(app_to_db, parameters)

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


def __get_by_number_journal_query(
    db: str, line_number: str, journal_entry_id: str
) -> tuple:
    """
    This function creates the select by line_number and journal_entry_id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    line_number: string
    This parameter specifies the line_number that will be used for this query

    journal_entry_id: string
    This parameter specifies the journal_entry_id that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """SELECT li.id, li.uuid, acc.uuid as account_id,
        acc.account_no, acc.name as account_name, li.journal_entry_id,
        li.line_number, li.memo, li.entity_id,
        li.posting_type, li.amount, li.created_at
        FROM """
        + db
        + """.line_item li
        INNER JOIN """
        + db
        + """.account acc ON (li.account_id = acc.id)
        where li.line_number = %s and li.journal_entry_id = %s;"""
    )

    params = (line_number, journal_entry_id)

    return (query, params)


def select_by_number_journal(
    db: str, line_number: str, journal_entry_id: str, region_name: str, secret_name: str
) -> dict:
    """
    This function returns the record from the result of the "select by number journal" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    line_number: string
    This parameter specifies the line_number that will be used for this query

    journal_entry_id: string
    This parameter specifies the journal_entry_id that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A dict containing the line item that matches with the upcoming line_number and journal_entry_id
    """
    params = __get_by_number_journal_query(db, line_number, journal_entry_id)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_single_record_select(conn, params)

    return record


def __get_by_journal_query(db: str, journal_entry_id: str) -> tuple:
    """
    This function creates the select line_number, uuid by journal_entry_id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    journal_entry_id: string
    This parameter specifies the journal_entry_id that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """SELECT li.id, li.uuid, acc.uuid as account_id,
        acc.account_no, acc.name as account_name, li.journal_entry_id,
        li.line_number, li.memo, li.entity_id,
        li.posting_type, li.amount, li.created_at
        FROM """
        + db
        + """.line_item li
        INNER JOIN """
        + db
        + """.account acc ON (li.account_id = acc.id)
        where li.journal_entry_id = %s;"""
    )

    params = (journal_entry_id,)

    return (query, params)


def select_by_journal(
    db: str, journal_entry_id: str, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select numbers by journal" query with its parameters.

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
    A dict containing the line items that match with the upcoming journal_entry_id
    """
    params = __get_by_journal_query(db, journal_entry_id)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def select_numbers_by_journal(
    db: str, journal_entry_id: str, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select numbers by journal" query with its parameters.

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
    A dict containing the line item's number and uuid that matches with the upcoming journal_entry_id
    """
    params = __get_by_journal_query(db, journal_entry_id)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    if records:
        ret_list = []
        for entry in records:
            ret_list.append(
                {"line_number": entry["line_number"], "uuid": entry["uuid"]}
            )

        return ret_list

    return None


def get_delete_query(db: str, id_: str) -> tuple:
    """
    This function creates the delete query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id: string
    This parameter specifies the uuid for the element to be deleted

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """
        DELETE FROM """
        + db
        + """.line_item
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
        + """.line_item
        WHERE journal_entry_id = %s;"""
    )

    params = (journal_entry_id,)

    return (query, params)


def __get_by_multiple_journals_query(db: str, journal_entry_ids: list) -> tuple:
    """
    This function creates the select by multiple journal_entry_id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    journal_entry_ids: string
    This parameter specifies the list of journal_entry_ids that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    format_strings = ",".join(["%s"] * len(journal_entry_ids))

    query = (
        """SELECT li.id, li.uuid, acc.uuid as account_id,
        acc.account_no, acc.name as account_name, li.journal_entry_id,
        li.line_number, li.memo, li.entity_id,
        li.posting_type, li.amount, li.created_at
        FROM """
        + db
        + """.line_item li INNER JOIN """
        + db
        + f".account acc ON (li.account_id = acc.id) WHERE li.journal_entry_id IN ({format_strings});"
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
    This parameter specifies the list of journal_entry_ids that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A dict containing the line items that match with the upcoming journal_entry_ids
    """
    params = __get_by_multiple_journals_query(db, journal_entry_ids)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def __get_by_account_id_query(db: str, account_id: str) -> tuple:
    """
    This function creates the select by account_id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_id: string
    This parameter specifies the account_id that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """SELECT li.id, li.uuid, acc.uuid as account_id,
        acc.account_no, acc.name as account_name, li.journal_entry_id,
        li.line_number, li.memo, li.entity_id,
        li.posting_type, li.amount, li.created_at
        FROM """
        + db
        + """.line_item li
        INNER JOIN """
        + db
        + """.account acc ON (li.account_id = acc.id)
        where li.account_id = %s;"""
    )

    params = (account_id,)

    return (query, params)


def select_by_account_id(
    db: str, account_id: str, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select by account_id" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_id: string
    This parameter specifies the account_id that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list of dicts containing the line items that match with the upcoming account_id
    """
    params = __get_by_account_id_query(db, account_id)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records

def __get_count_by_account_id_query(db: str, account_id: str) -> tuple:
    """
    This function creates the count by account_id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_id: string
    This parameter specifies the account_id that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """SELECT count(*)
        FROM """
        + db
        + """.line_item li
        INNER JOIN """
        + db
        + """.account acc ON (li.account_id = acc.id)
        where li.account_id = %s;"""
    )

    params = (account_id,)

    return (query, params)

def __get_by_account_id_query_with_offset(db: str, account_id: str, limit: str, offset: str) -> tuple:
    """
    This function creates the select by account_id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_id: string
    This parameter specifies the account_id that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """SELECT li.id, li.uuid, acc.uuid as account_id,
        acc.account_no, acc.name as account_name, li.journal_entry_id,
        li.line_number, li.memo, li.entity_id,
        li.posting_type, li.amount, li.created_at
        FROM """
        + db
        + """.line_item li
        INNER JOIN """
        + db
        + """.account acc ON (li.account_id = acc.id)
        where li.account_id = %s ORDER BY acc.uuid limit %s offset %s;"""
    )

    params = (account_id, limit, offset)

    return (query, params)

def select_count_by_account_id(
    db: str, account_id: str, region_name: str, secret_name: str
) -> tuple:
    """
    This function returns the record count from the result of the "select by account_id" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_id: string
    This parameter specifies the account_id that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list of dicts containing the line items that match with the upcoming account_id
    """
    params = __get_count_by_account_id_query(db, account_id)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_single_record_select(conn, params)

    return records

def select_by_account_id_with_offset(
    db: str, account_id: str, limit: str, offset:str, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select by account_id" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_id: string
    This parameter specifies the account_id that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list of dicts containing the line items that match with the upcoming account_id
    """
    params = __get_by_account_id_query_with_offset(db, account_id, limit, offset)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records