"""This module provides the Aurora MySQL serverless capabilities for line items"""
from . import db_main
from . import connection
from . import account

app_to_db = {
    "lineItemNo": "line_number",
    "accountNo": "account_number",
    "entryMemo": "memo",
    "amount": "amount",
    "txMemo": "memo",
    "adjustingJournalEntry": "adjusting_journal_entry",
    "state": "state",
    "VendorCustomerPartner": "vendor_customer_partner",
}


def get_insert_query(
    db: str,
    input: dict,
    journal_entry_id: str,
    posting_type: str,
    region_name: str,
    secret_name: str,
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
        + """.line_item
            (uuid, account_id, journal_entry_id, line_number, memo, posting_type,
            state, is_hidden, vendor_customer_partner_type, vendor_customer_partner_id)
        VALUES
            (%s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s);"""
    )

    translated_input = db_main.translate_to_db(app_to_db, input)

    account_number = translated_input.get("account_number")
    account_id = account.get_id(db, account_number, region_name, secret_name)

    # Getting new uuid from the db to return it in insertion
    ro_conn = connection.get_connection(db, region_name, secret_name, "ro")
    uuid = db_main.get_new_uuid(ro_conn)

    params = (
        uuid,
        account_id,
        journal_entry_id,
        translated_input.get("line_number"),
        translated_input.get("memo"),
        translated_input.get("state"),
        posting_type,
        translated_input.get("is_hidden"),
        translated_input.get("vendor_customer_partner").get("VCPtype"),
        translated_input.get("vendor_customer_partner").get("VCPId"),
    )

    return (query, params)


def get_update_query(db: str, id: str, input: dict) -> tuple:
    """
    This function creates the update query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id: string
    This parameter specifies the uuid for identifying the line item
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
        + """.line_item
        SET """
    )
    where_clause = "WHERE uuid = %s;"

    translated_input = db_main.translate_to_db(app_to_db, input)

    set_clause = ""
    params = ()
    for key in translated_input.keys():
        set_clause += str(key) + " = %s,\n"
        params += (translated_input.get(key),)

    size = len(set_clause)
    # Slice string to remove last 3 characters from string
    set_clause = set_clause[: size - 2]
    set_clause += "\n "

    params += (id,)

    query = update_query + set_clause + where_clause

    return (query, params)


def get_by_number_journal_query(
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
        "SELECT * FROM "
        + db
        + ".line_item where line_number = %s and journal_entry_id = %s;"
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
    params = get_by_number_journal_query(db, line_number, journal_entry_id)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_single_record_select(conn, params)

    return record


def get_numbers_by_journal_query(db: str, journal_entry_id: str) -> tuple:
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
        "SELECT line_number, uuid FROM "
        + db
        + ".line_item where journal_entry_id = %s;"
    )

    params = (journal_entry_id,)

    return (query, params)


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
    params = get_numbers_by_journal_query(db, journal_entry_id)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def get_delete_query(db: str, id: str) -> tuple:
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

    params = (id,)

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

    params = (id,)

    return (query, params)


def insert(db: str, input: dict, region_name: str, secret_name: str) -> None:
    """
    This function executes the insert query with its parameters.

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

    db_type: string (Optional)
    This parameter when set with 'ro' value is used to point the
    read only queries to a specific read only endpoint that will
    be optimized for this type of operations

    return
    A string specifying the recently added journal entry's uuid
    """
    params = get_insert_query(db, input, region_name, secret_name)

    query_params = [params[0], params[1]]

    conn = connection.get_connection(db, region_name, secret_name)

    query_list = [query_params]

    db_main.execute_dml(conn, query_list)

    return


def delete(db: str, id: str, region_name: str, secret_name: str) -> None:
    """
    This function executes the delete query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id: string
    This parameter contains the uuid of the line item that will be deleted

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    db_type: string (Optional)
    This parameter when set with 'ro' value is used to point the
    read only queries to a specific read only endpoint that will
    be optimized for this type of operations
    """
    params = get_delete_query(db, id)

    conn = connection.get_connection(db, region_name, secret_name)

    query_list = [(params[0], params[1])]

    db_main.execute_dml(conn, query_list)


def delete_by_journal(
    db: str, journal_entry_id: str, region_name: str, secret_name: str
) -> None:
    """
    This function executes the delete by journal_entry_id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    journal_entry_id: string
    This parameter contains the journal_entry_id of the element/s that will be deleted

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    db_type: string (Optional)
    This parameter when set with 'ro' value is used to point the
    read only queries to a specific read only endpoint that will
    be optimized for this type of operations
    """
    params = get_delete_by_journal_query(db, journal_entry_id)

    conn = connection.get_connection(db, region_name, secret_name)

    query_list = [(params[0], params[1])]

    db_main.execute_dml(conn, query_list)


def update(db: str, id: str, input: dict, region_name: str, secret_name: str) -> None:
    """
    This function executes the update query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    uuid: string
    This parameter specifies the uuid of the line_item that will be updated

    input: dictionary
    This parameter contains all the parameters inside a dictionary that
    will be used for the query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    db_type: string (Optional)
    This parameter when set with 'ro' value is used to point the
    read only queries to a specific read only endpoint that will
    be optimized for this type of operations
    """
    params = get_update_query(db, id, input)

    conn = connection.get_connection(db, region_name, secret_name)

    query_list = [(params[0], params[1])]

    db_main.execute_dml(conn, query_list)
