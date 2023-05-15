"""This module provides the Aurora MySQL serverless capabilities for journal entries"""
from . import db_main
from . import connection
from . import ledger
from . import line_item


app_to_db = {
    "journalId": "uuid",
    "ledgerId": "ledger_id",
    "txReference": "reference",
    "txMemo": "memo",
    "adjustingJournalEntry": "adjusting_journal_entry",
    "state": "state",
    "isHidden": "is_hidden",
}


def __get_insert_query(db: str, input: dict, region_name: str, secret_name: str) -> tuple:
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
        + """.journal_entry
            (uuid, ledger_id, reference, memo, adjusting_journal_entry, state, is_hidden)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s);"""
    )

    translated_input = db_main.translate_to_db(app_to_db, input)

    ledger_uuid = translated_input.get("ledger_id")
    ledger_id = ledger.get_id(db, ledger_uuid, region_name, secret_name)

    # Getting new uuid from the db to return it in insertion
    ro_conn = connection.get_connection(db, region_name, secret_name, "ro")
    uuid = db_main.get_new_uuid(ro_conn)

    params = (
        uuid,
        ledger_id,
        translated_input.get("reference"),
        translated_input.get("memo"),
        translated_input.get("adjusting_journal_entry"),
        translated_input.get("state"),
        translated_input.get("is_hidden"),
    )

    return (query, params, uuid)


def __get_update_query(db: str, id: str, input: dict) -> tuple:
    """
    This function creates the update query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id: string
    This parameter specifies the uuid for identifying the journal entry
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
        + """.journal_item
        SET """
    )
    where_clause = "WHERE uuid = %s;"

    translated_input = db_main.translate_to_db(app_to_db, input)

    if "debitEntries" in translated_input:
        del translated_input["debitEntries"]
    if "creditEntries" in translated_input:
        del translated_input["creditEntries"]

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


def __get_delete_query(db: str, id: str) -> tuple:
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
        + """.journal_entry
        WHERE uuid = %s;"""
    )

    params = (id,)

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
    query = "SELECT * FROM " + db + ".journal_entry where uuid = %s;"

    params = (uuid,)

    return (query, params)

def __get_select_committed_between_dates_query(db: str, start_date: str, end_date:str) -> tuple:
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
    query = "SELECT * FROM " + db + ".journal_entry where state = 'COMMITTED' and (post_date BETWEEN %s and %s);"

    params = (start_date, end_date,)

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

def select_committed_between_dates(db: str, start_date: str, end_date: str, region_name: str, secret_name: str) -> list:
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
    params = __get_select_committed_between_dates_query(db, start_date, end_date)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_multiple_record_select(conn, params)

    return record


def insert(db: str, input: dict, region_name: str, secret_name: str) -> str:
    """
    This function executes the insert query with its parameters.
    It will also insert all its related line_items.

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
    params = __get_insert_query(db, input, region_name, secret_name)
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
        for debit_entry in input["debitEntries"]:
            entry_params = line_item.get_insert_query(
                    db, debit_entry, journal_entry_id, "Debit", region_name, secret_name
                )
            cursor.execute(entry_params[0], entry_params[1])

        for credit_entry in input["creditEntries"]:
            entry_params = line_item.get_insert_query(
                    db, credit_entry, journal_entry_id, "Credit", region_name, secret_name
                )
            cursor.execute(entry_params[0], entry_params[1])

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

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
    id = select_by_uuid(db, uuid, region_name, secret_name).get("id")

    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor()

    try:
        # Executing delete of journal entry first
        cursor.execute(query, q_params)

        # Once deleted, delete the line items by journal_entry_id
        entry_params = line_item.get_delete_by_journal_query(db, id, region_name, secret_name)
        cursor.execute(entry_params[0], entry_params[1])

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

    return


def update(db: str, uuid: str, input: dict, region_name: str, secret_name: str) -> None:
    """
    This function executes the update query with its parameters.
    It will also upsert all its related line_items.

    db: string
    This parameter specifies the db name where the query will be executed

    uuid: string
    This parameter specifies the uuid of the journal_entry that will be updated

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
    params = __get_update_query(db, uuid, input, region_name, secret_name)
    query = params[0]
    q_params = params[1]

    # Getting the id before updating
    journal_entry_id = select_by_uuid(db, uuid, region_name, secret_name).get("id")

    # Getting the line_number, uuid from all the line items for this journal
    lines_list = line_item.select_numbers_by_journal(
        db, journal_entry_id, region_name, secret_name
    )

    # Getting only the line_number for iterating later
    list_line_numbers = [
        key.get("line_number")
        for key in lines_list
        if key.get("line_number") is not None
    ]

    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor()

    try:
        # Executing update of journal entry first
        cursor.execute(query, q_params)

        # Then, upsert debit and credit entries
        if "debitEntries" in input:
            for debit_entry in input["debitEntries"]:
                line_uuid = None

                # Filtering to decide if it is insert/update
                if debit_entry["lineItemNo"] in list_line_numbers:
                    # Getting the uuid from the line_item
                    line_uuid = next(
                        (
                            x
                            for x in lines_list
                            if x.get("line_number") == debit_entry["lineItemNo"]
                        ),
                        None,
                    ).get("uuid")
                    entry_params = line_item.get_update_query(db, line_uuid, debit_entry)
                else:
                    entry_params = line_item.get_insert_query(
                        db,
                        credit_entry,
                        journal_entry_id,
                        "Debit",
                        region_name,
                        secret_name,
                    )
                
                cursor.execute(entry_params[0], entry_params[1])

        if "creditEntries" in input:
            for credit_entry in input["creditEntries"]:
                line_uuid = None

                # Filtering to decide if it is insert/update
                if credit_entry["lineItemNo"] in list_line_numbers:
                    # Getting the uuid from the line_item
                    line_uuid = next(
                        (
                            x
                            for x in lines_list
                            if x.get("line_number") == credit_entry["lineItemNo"]
                        ),
                        None,
                    ).get("uuid")
                    entry_params = line_item.get_update_query(db, line_uuid, credit_entry)
                else:
                    entry_params = line_item.get_insert_query(
                        db,
                        credit_entry,
                        journal_entry_id,
                        "Credit",
                        region_name,
                        secret_name,
                    )
                
                cursor.execute(entry_params[0], entry_params[1])

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

    return
