"""This module provides the Aurora MySQL serverless capabilities for journal entries"""

from . import db_main
from . import connection
from . import ledger
from . import line_item
from . import attachment


app_to_db = {
    "id": "id",
    "journalEntryId": "uuid",
    "journalEntryNum": "journal_entry_num",
    "ledgerId": "ledger_id",
    "reference": "reference",
    "memo": "memo",
    "adjustingJournalEntry": "adjusting_journal_entry",
    "state": "state",
    "isHidden": "is_hidden",
    "postDate": "post_date",
    "date": "date",
    "attachments": "attachments",
    "lineItems": "line_items",
}


def __get_insert_query(
    db: str, input_: dict, region_name: str, secret_name: str
) -> tuple:
    """
    This function creates the insert query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    input_: dictionary
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
        + """.journal_entry
            (uuid, ledger_id, reference, memo, adjusting_journal_entry, state, is_hidden, journal_entry_num)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s);"""
    )

    translated_input = db_main.translate_to_db(app_to_db, input_)

    ledger_uuid = translated_input.get("ledger_id")
    ledger_id = ledger.get_id(db, ledger_uuid, region_name, secret_name)

    # Getting new uuid from the db to return it in insertion
    ro_conn = connection.get_connection(db, region_name, secret_name, "ro")
    uuid = db_main.get_new_uuid(ro_conn)

    # Getting max journal_entry_num +1 by ledger_id
    journal_entry_num = select_max_number_by_ledger(
        db, ledger_id, region_name, secret_name
    )

    params = (
        uuid,
        ledger_id,
        translated_input.get("reference"),
        translated_input.get("memo"),
        translated_input.get("adjusting_journal_entry"),
        translated_input.get("state"),
        translated_input.get("is_hidden"),
        journal_entry_num,
    )

    return (query, params, uuid)


def __get_update_query(db: str, id_: str, input_: dict) -> tuple:
    """
    This function creates the update query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id_: string
    This parameter specifies the uuid for identifying the journal entry
    that will be updated

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
        + """.journal_entry
        SET """
    )
    where_clause = "WHERE uuid = %s;"

    translated_input = db_main.translate_to_db(app_to_db, input_)

    if "line_items" in translated_input:
        del translated_input["line_items"]
    if "attachments" in translated_input:
        del translated_input["attachments"]

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


def __get_delete_query(db: str, id_: str) -> tuple:
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
        + """.journal_entry
        WHERE uuid = %s;"""
    )

    params = (id_,)

    return (query, params)


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
    query = (
        """SELECT je.id, je.journal_entry_num, je.uuid, le.uuid as ledger_id,
    je.date, je.reference, je.memo, je.adjusting_journal_entry,
    je.state, je.is_hidden, je.post_date, je.created_at
    FROM """
        + db
        + """.journal_entry je
    INNER JOIN """
        + db
        + """.ledger le ON (je.ledger_id = le.id)
    where je.uuid = %s;"""
    )

    params = (uuid,)

    return (query, params)


def __get_select_by_ledger_uuid_query(db: str, ledger_uuid: str) -> tuple:
    """
    This function creates the select by ledger query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    ledger_uuid: string
    This parameter specifies the ledger_uuid that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """SELECT je.id, je.journal_entry_num, je.uuid, le.uuid as ledger_id,
    je.date, je.reference, je.memo, je.adjusting_journal_entry,
    je.state, je.is_hidden, je.post_date, je.created_at
    FROM """
        + db
        + """.journal_entry je
    INNER JOIN """
        + db
        + """.ledger le ON (je.ledger_id = le.id)
    where le.uuid = %s;"""
    )

    params = (ledger_uuid,)

    return (query, params)


def __get_select_posted_between_dates_query(
    db: str, start_date: str, end_date: str
) -> tuple:
    """
    This function creates the select between dates for commited state journal entries.

    db: string
    This parameter specifies the db name where the query will be executed

    start_date: string
    This parameter specifies the start date that will be used for this query

    end_date: string
    This parameter specifies the end date that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        "SELECT * FROM "
        + db
        + ".journal_entry where state = 'POSTED' and (post_date BETWEEN %s and %s);"
    )

    params = (
        start_date,
        end_date,
    )

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
    A dict containing the journal entry that matches with the upcoming uuid
    """
    params = __get_select_by_uuid_query(db, uuid)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_single_record_select(conn, params)

    return record


def select_by_ledger_uuid(
    db: str, ledger_uuid: str, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select by ledger uuid" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    ledger_uuid: string
    This parameter specifies the ledger_uuid that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list containing the journal entries that match with the upcoming ledger_id
    """
    params = __get_select_by_ledger_uuid_query(db, ledger_uuid)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def select_posted_between_dates(
    db: str, start_date: str, end_date: str, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select by uuid" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    start_date: string
    This parameter specifies the start date that will be used for this query

    end_date: string
    This parameter specifies the end date that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A dict containing the journal entry that matches with the upcoming uuid
    """
    params = __get_select_posted_between_dates_query(db, start_date, end_date)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_multiple_record_select(conn, params)

    return record


def insert(db: str, input_: dict, region_name: str, secret_name: str) -> str:
    """
    This function executes the insert query with its parameters.
    It will also insert all its related line_items.

    db: string
    This parameter specifies the db name where the query will be executed

    input_: dictionary
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
    params = __get_insert_query(db, input_, region_name, secret_name)
    query = params[0]
    q_params = params[1]
    uuid = params[2]

    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor()

    try:
        # Executing insert of journal entry first
        cursor.execute(query, q_params)

        # Once inserted, get the auto-generated id
        journal_entry_id = cursor.lastrowid

        # Then, insert debit and credit entries
        if "lineItems" in input_:
            for item in input_["lineItems"]:
                type_ = item.pop("type")
                line_number_ = str(input_["lineItems"].index(item) + 1)
                entry_params = line_item.get_insert_query(
                    db,
                    item,
                    journal_entry_id,
                    line_number_,
                    type_,
                    region_name,
                    secret_name,
                )
                cursor.execute(entry_params[0], entry_params[1])

        # Also, insert attachments
        if "attachments" in input_:
            for att in input_["attachments"]:
                att_params = attachment.get_insert_query(db, att, journal_entry_id)
                cursor.execute(att_params[0], att_params[1])

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

    return uuid


def delete(db: str, uuid: str, region_name: str, secret_name: str) -> None:
    """
    This function executes the delete query with its parameters.
    It will also delete all its related line_items.

    db: string
    This parameter specifies the db name where the query will be executed

    uuid: string
    This parameter contains the uuid of the journal entry that will be deleted

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
    params = __get_delete_query(db, uuid)
    query = params[0]
    q_params = params[1]

    # Getting the id before deleting
    id_ = select_by_uuid(db, uuid, region_name, secret_name).get("id")

    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor()

    try:
        # First, delete the line items by journal_entry_id
        entry_params = line_item.get_delete_by_journal_query(db, id_)
        cursor.execute(entry_params[0], entry_params[1])

        # Then, delete the attachments by journal_entry_id
        att_params = attachment.get_delete_by_journal_query(db, id_)
        cursor.execute(att_params[0], att_params[1])

        # Finally delete the journal entry
        cursor.execute(query, q_params)

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()


def update(db: str, uuid: str, input_: dict, region_name: str, secret_name: str) -> None:
    """
    This function executes the update query with its parameters.
    It will also upsert all its related line_items.

    db: string
    This parameter specifies the db name where the query will be executed

    uuid: string
    This parameter specifies the uuid of the journal_entry that will be updated

    input_: dictionary
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
    params = __get_update_query(db, uuid, input_)
    query = params[0]
    q_params = params[1]

    # Getting the id before updating
    journal_entry_id = select_by_uuid(db, uuid, region_name, secret_name).get("id")

    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor()

    try:
        if len(q_params) > 1:
            # Executing update of journal entry first
            cursor.execute(query, q_params)

        # Then, insert debit and credit entries
        if "lineItems" in input_:
            # Once updated, delete all its line_items and attachments
            # and keep only the upcoming ones (if these exist)
            del_entry_params = line_item.get_delete_by_journal_query(db, journal_entry_id)
            cursor.execute(del_entry_params[0], del_entry_params[1])

            for item in input_["lineItems"]:
                type_ = item.pop("type")
                line_number_ = str(input_["lineItems"].index(item) + 1)
                entry_params = line_item.get_insert_query(
                    db,
                    item,
                    journal_entry_id,
                    line_number_,
                    type_,
                    region_name,
                    secret_name,
                )
                cursor.execute(entry_params[0], entry_params[1])

        # Also, insert attachments
        if "attachments" in input_:
            del_att_params = attachment.get_delete_by_journal_query(db, journal_entry_id)
            cursor.execute(del_att_params[0], del_att_params[1])

            for att in input_["attachments"]:
                att_params = attachment.get_insert_query(db, att, journal_entry_id)
                cursor.execute(att_params[0], att_params[1])

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()


def __get_count_with_post_date(db: str) -> tuple:
    """
    This function creates the select query that counts the amount of rows with post_date not null.

    db: string
    This parameter specifies the db name where the query will be executed

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """

    query = (
        """
        SELECT count(*)
        FROM """
        + db
        + """.journal_entry
        where post_date IS NOT NULL;"""
    )

    params = ()

    return (query, params)


def select_count_with_post_date(db: str, region_name: str, secret_name: str) -> dict:
    """
    This function returns the record from the result of the "select count with post date" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A dict containing the count
    """
    params = __get_count_with_post_date(db)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_single_record_select(conn, params)

    return record


def __get_max_number_by_ledger_query(db: str, ledger_id: str) -> tuple:
    """
    This function creates the select max journal number by ledger_id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    ledger_id: string
    This parameter specifies the ledger_id that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """SELECT IFNULL(MAX(je.journal_entry_num),0) AS journal_entry_num
    FROM """
        + db
        + """.journal_entry je
    where je.ledger_id = %s;"""
    )

    params = (ledger_id,)

    return (query, params)


def select_max_number_by_ledger(
    db: str, ledger_id: str, region_name: str, secret_name: str
) -> str:
    """
    This function returns the record from the result of the "select max number by ledger" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    ledger_id: string
    This parameter specifies the ledger_id that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A string containing the new max journal entry number by the upcoming ledger
    """
    params = __get_max_number_by_ledger_query(db, ledger_id)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_single_record_select(conn, params)

    new_num = int(record.get("journal_entry_num")) + 1

    return str(new_num)


def __get_select_by_fund_id_query(db: str, fund_id: str) -> tuple:
    """
    This function creates the select by fund query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    fund_id: string
    This parameter specifies the fund_id that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """SELECT je.id, je.journal_entry_num, je.uuid, le.uuid as ledger_id,
    je.date, je.reference, je.memo, je.adjusting_journal_entry,
    je.state, je.is_hidden, je.post_date, je.created_at
    FROM """
        + db
        + """.journal_entry je
    INNER JOIN """
        + db
        + """.ledger le ON (je.ledger_id = le.id)
    INNER JOIN """
        + db
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
    where fe.uuid = %s;"""
    )

    params = (fund_id,)

    return (query, params)


def select_by_fund_id(
    db: str, fund_id: str, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select by fund id" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    fund_id: string
    This parameter specifies the fund_id that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list containing the journal entries that match with the upcoming ledger_id
    """
    params = __get_select_by_fund_id_query(db, fund_id)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def __get_select_by_client_id_query(db: str, client_id: str) -> tuple:
    """
    This function creates the select by client query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    client_id: string
    This parameter specifies the client_id that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """SELECT je.id, je.journal_entry_num, je.uuid, le.uuid as ledger_id,
    je.date, je.reference, je.memo, je.adjusting_journal_entry,
    je.state, je.is_hidden, je.post_date, je.created_at
    FROM """
        + db
        + """.journal_entry je
    INNER JOIN """
        + db
        + """.ledger le ON (je.ledger_id = le.id)
    INNER JOIN """
        + db
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
    where fe.client_id = %s;"""
    )

    params = (client_id,)

    return (query, params)


def select_by_client_id(
    db: str, client_id: str, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select by client id" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    client_id: string
    This parameter specifies the client_id that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list containing the journal entries that match with the upcoming ledger_id
    """
    params = __get_select_by_client_id_query(db, client_id)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records
