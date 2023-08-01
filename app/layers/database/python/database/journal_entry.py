"""This module provides the Aurora MySQL serverless capabilities for journal entries"""

import math
from . import db_main
from . import connection
from . import ledger
from . import line_item
from . import attachment
from pymysql.cursors import Cursor, DictCursor
from typing import Union
from datetime import datetime
from shared import dataclass_encoder

app_to_db = {
    "id": "id",
    "journalEntryId": "uuid",
    "journalEntryNum": "journal_entry_num",
    "ledgerId": "ledger_id",
    "reference": "reference",
    "memo": "memo",
    "adjustingJournalEntry": "adjusting_journal_entry",
    "state": "state",
    "postDate": "post_date",
    "date": "date",
    "attachments": "attachments",
    "lineItems": "line_items",
    "currencyName": "currency",
    "currencyDecimal": "decimals",
    "fundId": "fund_entity_id",
    "ledgerState": "ledger_state",
    "accountState": "account_state",
    "accountId": "account_id"
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
            (uuid, ledger_id, reference, memo, adjusting_journal_entry, state, journal_entry_num, date)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s);"""
    )

    translated_input = db_main.translate_to_db(app_to_db, input_)

    ledger_uuid = translated_input.get("ledger_id")
    ledger_id = ledger.get_id(db, ledger_uuid, region_name, secret_name)

    # Getting new uuid from the db to return it in insertion
    uuid = db_main.get_new_uuid()

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
        journal_entry_num,
        translated_input.get("date"),
    )

    return (query, params, uuid)


def __get_update_query(db: str, id_: str, input_: dict, region_name, secret_name) -> tuple:
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

    region_name: aws region

    secret_name: name of the db secret_name

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

    if "ledger_id" in translated_input:
        translated_input["ledger_id"] = ledger.get_id(db, translated_input["ledger_id"], region_name, secret_name)
        translated_input["journal_entry_num"] = select_max_number_by_ledger(
            db, translated_input["ledger_id"], region_name, secret_name
        )

    for key, value in translated_input.items():
        set_clause += str(key) + " = %s,\n"
        params += (value,)

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
    je.state, je.post_date, je.created_at, le.currency, le.decimals,
    fe.uuid as fund_entity_id
    FROM """
        + db
        + """.journal_entry je
    INNER JOIN """
        + db
        + """.ledger le ON (je.ledger_id = le.id)
    INNER JOIN """
        + db
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
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
    je.state, je.post_date, je.created_at, le.currency, le.decimals,
    fe.uuid as fund_entity_id
    FROM """
        + db
        + """.journal_entry je
    INNER JOIN """
        + db
        + """.ledger le ON (je.ledger_id = le.id)
    INNER JOIN """
        + db
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
    where le.uuid = %s;"""
    )

    params = (ledger_uuid,)

    return (query, params)


def __get_numbers_by_ledger_uuid_query(db: str, ledger_uuid: str) -> tuple:
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
        """SELECT je.journal_entry_num
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


def __get_select_by_ledger_uuid_query_paginated(
    db: str,
    ledger_uuid: str,
    limit: int,
    offset: int) -> tuple:
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
    je.state, je.post_date, je.created_at, le.currency, le.decimals,
    fe.uuid as fund_entity_id
    FROM """
        + db
        + """.journal_entry je
    INNER JOIN """
        + db
        + """.ledger le ON (je.ledger_id = le.id)
    INNER JOIN """
        + db
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
    WHERE le.uuid = %s LIMIT %s OFFSET %s;"""
    )

    params = (ledger_uuid, limit, offset,)

    return (query, params)


def __get_total_by_ledger_uuid_query(db: str, ledger_uuid: str):
    query = (
        """SELECT COUNT(1)
    FROM """
        + db
        + """.journal_entry je
    INNER JOIN """
        + db
        + """.ledger le ON (je.ledger_id = le.id)
    INNER JOIN """
        + db
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
    WHERE le.uuid = %s;"""
    )

    params = (ledger_uuid, )

    return (query, params)


def __get_select_by_ledger_uuid_with_order_query(db: str, ledger_uuid: str, order_list: list) -> tuple:
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
    format_strings = ",".join(["%s"] * len(order_list))

    query = (
        """SELECT je.id, je.journal_entry_num, je.uuid, le.uuid as ledger_id,
    je.date, je.reference, je.memo, je.adjusting_journal_entry,
    je.state, je.post_date, je.created_at, le.currency, le.decimals,
    fe.uuid as fund_entity_id
    FROM """
        + db
        + """.journal_entry je
    INNER JOIN """
        + db
        + """.ledger le ON (je.ledger_id = le.id)
    INNER JOIN """
        + db
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
    where le.uuid = %s ORDER BY %s;"""
    )

    params = (ledger_uuid, format_strings)

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


def __get_select_ids_by_uuid_list_query(db, uuid_list):

    query = (
        "SELECT id, uuid FROM "
        + db
        + f".journal_entry WHERE uuid in ({','.join(['%s'] * len(uuid_list))});"
    )

    params = tuple(uuid_list)

    return (query, params)


def select_ids_by_uuid_list(
    db: str, uuid_list: str, region_name: str, secret_name: str
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
    params = __get_select_ids_by_uuid_list_query(db, uuid_list)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    lookup = {r['uuid']: r['id'] for r in records}
    return lookup



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


def select_by_ledger_uuid_paginated(
    db: str,
    ledger_uuid: str,
    region_name: str,
    secret_name: str,
    page: int,
    page_size: int
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
    offset = (page - 1) * page_size

    params = __get_select_by_ledger_uuid_query_paginated(db, ledger_uuid, page_size, offset)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    total_params = __get_total_by_ledger_uuid_query(db, ledger_uuid)

    record = db_main.execute_single_record_select(conn, total_params)

    total_records = list(record.values())[0]

    total_pages = math.ceil(total_records / page_size)

    return (records, page, total_pages, total_records)


def select_by_ledger_uuid_with_order(
    db: str, ledger_uuid: str, order_list: list, region_name: str, secret_name: str
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
    params = __get_select_by_ledger_uuid_with_order_query(db, ledger_uuid, order_list)

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
    It will also delete all its related line_items and attachments.

    db: string
    This parameter specifies the db name where the query will be executed

    uuid: string
    This parameter contains the uuid of the journal entry that will be deleted

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials
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


def bulk_delete(db: str, uuids: list, region_name: str, secret_name: str) -> None:
    """
    This function executes the delete query with its parameters.
    It will also delete all its related line_items and attachments.

    db: string
    This parameter specifies the db name where the query will be executed

    uuids: list
    This parameter contains a list of uuids for journal entries that will be deleted

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials
    """
    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor()

    try:
        journal_query = None
        journal_params = []
        line_items_query = None
        line_items_params = []
        attachments_query = None
        attachments_params = []

        je_id_lookup = select_ids_by_uuid_list(db, uuids, region_name, secret_name)
        for uuid in uuids:
            params = __get_delete_query(db, uuid)
            if journal_query is None:
                journal_query = params[0]
            journal_params.append(params[1])

            # Getting the id before deleting
            id_ = je_id_lookup[uuid]

            # First, delete the line items by journal_entry_id
            li_params = line_item.get_delete_by_journal_query(db, id_)
            if line_items_query is None:
                line_items_query = li_params[0]
            line_items_params.append(li_params[1])

            # Then, delete the attachments by journal_entry_id
            att_params = attachment.get_delete_by_journal_query(db, id_)
            if attachments_query is None:
                attachments_query = att_params[0]
            attachments_params.append(att_params[1])

        cursor.executemany(line_items_query, line_items_params)
        cursor.executemany(attachments_query, attachments_params)
        cursor.executemany(journal_query, journal_params)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()


def update(
    db: str, uuid: str, input_: dict, region_name: str, secret_name: str
) -> None:
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
    """
    params = __get_update_query(db, uuid, input_, region_name, secret_name)
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
            del_entry_params = line_item.get_delete_by_journal_query(
                db, journal_entry_id
            )
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
            del_att_params = attachment.get_delete_by_journal_query(
                db, journal_entry_id
            )
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
    je.state, je.post_date, je.created_at, le.currency, le.decimals,
    fe.uuid as fund_entity_id
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


def __get_select_by_fund_id_query_paginated(
    db: str,
    fund_id: str,
    limit: int,
    offset: int) -> tuple:
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
    je.state, je.post_date, je.created_at, le.currency, le.decimals,
    fe.uuid as fund_entity_id
    FROM """
        + db
        + """.journal_entry je
    INNER JOIN """
        + db
        + """.ledger le ON (je.ledger_id = le.id)
    INNER JOIN """
        + db
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
    WHERE fe.uuid = %s LIMIT %s OFFSET %s;"""
    )

    params = (fund_id, limit, offset, )

    return (query, params)


def __get_total_by_fund_id_query(
    db: str,
    fund_id: str) -> tuple:
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
        """SELECT COUNT(1)
    FROM """
        + db
        + """.journal_entry je
    INNER JOIN """
        + db
        + """.ledger le ON (je.ledger_id = le.id)
    INNER JOIN """
        + db
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
    WHERE fe.uuid = %s;"""
    )

    params = (fund_id, )

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


def select_by_fund_id_paginated(
    db: str,
    fund_id: str,
    region_name: str,
    secret_name: str,
    page: int,
    page_size: int
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
    offset = (page - 1) * page_size

    params = __get_select_by_fund_id_query_paginated(db, fund_id, page_size, offset)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    total_params = __get_total_by_fund_id_query(db, fund_id)

    record = db_main.execute_single_record_select(conn, total_params)

    total_records = list(record.values())[0]

    total_pages = math.ceil(total_records / page_size)

    return (records, page, total_pages, total_records)


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
    je.state, je.post_date, je.created_at, le.currency, le.decimals,
    fe.uuid as fund_entity_id
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


def __get_select_by_client_id_query_paginated(
    db: str,
    client_id: str,
    limit: int,
    offset: int) -> tuple:
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
    je.state, je.post_date, je.created_at, le.currency, le.decimals,
    fe.uuid as fund_entity_id
    FROM """
        + db
        + """.journal_entry je
    INNER JOIN """
        + db
        + """.ledger le ON (je.ledger_id = le.id)
    INNER JOIN """
        + db
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
    WHERE fe.client_id = %s LIMIT %s OFFSET %s;"""
    )

    params = (client_id, limit, offset, )

    return (query, params)


def __get_total_by_client_id_query(
    db: str,
    client_id: str) -> tuple:
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
        """SELECT COUNT(1)
    FROM """
        + db
        + """.journal_entry je
    INNER JOIN """
        + db
        + """.ledger le ON (je.ledger_id = le.id)
    INNER JOIN """
        + db
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
    WHERE fe.client_id = %s;"""
    )

    params = (client_id, )

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


def select_by_client_id_paginated(
    db: str,
    client_id: str,
    region_name: str,
    secret_name: str,
    page: int,
    page_size: int
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
    offset = (page - 1) * page_size

    params = __get_select_by_client_id_query_paginated(db, client_id, page_size, offset)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    total_params = __get_total_by_client_id_query(db, client_id)

    record = db_main.execute_single_record_select(conn, total_params)

    total_records = list(record.values())[0]

    total_pages = math.ceil(total_records / page_size)

    return (records, page, total_pages, total_records)


def select_max_number_by_ledger_with_cursor(
    db: str, ledger_id: str, cursor: Union[Cursor, DictCursor]
) -> str:
    """
    This function returns the record from the result of the "select max number by ledger" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    ledger_id: string
    This parameter specifies the ledger_id that will be used for this query

    cursor: Cursor
    This parameter is a pymysql.cursors that specifies
    which cursor will be used to execute the query

    return
    A string containing the new max journal entry number by the upcoming ledger
    """
    params = __get_max_number_by_ledger_query(db, ledger_id)

    record = db_main.execute_single_record_select_with_cursor(cursor, params)

    new_num = int(record.get("journal_entry_num")) + 1

    return str(new_num)


def __get_insert_query_with_cursor(
    db: str,
    input_: dict,
    region_name: str,
    secret_name: str,
    cursor: Union[Cursor, DictCursor],
    ledger_lookup={},
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

    cursor: Cursor
    This parameter is a pymysql.cursors that specifies
    which cursor will be used to execute the query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """
        INSERT INTO """
        + db
        + """.journal_entry
            (uuid, ledger_id, reference, memo, adjusting_journal_entry, state, journal_entry_num, date)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s);"""
    )

    translated_input = db_main.translate_to_db(app_to_db, input_)

    ledger_uuid = translated_input.get("ledger_id")
    ledger_id = ledger_lookup.get(ledger_uuid)
    if ledger_id is None:
        ledger_id = ledger.get_id(db, ledger_uuid, region_name, secret_name)
        ledger_lookup[ledger_uuid] = ledger_id

    uuid = db_main.get_new_uuid()

    # Try to get the journal_entry_num from the input first
    journal_entry_num = translated_input.get("journal_entry_num")
    if not journal_entry_num:
        # Getting max journal_entry_num +1 by ledger_id
        journal_entry_num = select_max_number_by_ledger_with_cursor(
            db, ledger_id, cursor
        )

    params = (
        uuid,
        ledger_id,
        translated_input.get("reference"),
        translated_input.get("memo"),
        translated_input.get("adjusting_journal_entry"),
        translated_input.get("state"),
        journal_entry_num,
        translated_input.get("date"),
    )

    return (query, params, uuid)


def bulk_insert(db: str, input_list: dict, region_name: str, secret_name: str) -> list:
    """
    This function executes the bulk insert query with its parameters.
    It will also insert all its related line_items.

    db: string
    This parameter specifies the db name where the query will be executed

    input_list: list
    This parameter contains a list with all the parameters inside
    a dictionary that will be used for the query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list of strings specifying the recently added journal entries' uuids
    """
    uuids_list = []

    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor(DictCursor)

    try:
        # account_id_lookup with hold references to account UUIDs to incremental IDs
        # so we don't have to repeatedly query the database
        account_id_lookup = {}
        ledger_lookup = {}

        line_items_params = []
        line_items_query = None
        attachments_params = []
        attachments_query = None
        for input_ in input_list:
            params = __get_insert_query_with_cursor(
                db, input_, region_name, secret_name, cursor, ledger_lookup
            )

            query = params[0]
            q_params = params[1]
            uuid = params[2]

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
                        account_id_lookup
                    )

                    if line_items_query is None:
                        line_items_query = entry_params[0]

                    line_items_params.append(entry_params[1])

            # Also, insert attachments
            if "attachments" in input_:
                for att in input_["attachments"]:
                    att_params = attachment.get_insert_query(db, att, journal_entry_id)

                    if attachments_query is None:
                        attachments_query = att_params[0]

                    attachments_params.append(att_params[1])

            uuids_list.append(uuid)

        cursor.executemany(line_items_query, line_items_params)
        cursor.executemany(attachments_query, attachments_params)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

    return uuids_list


def select_by_uuid_with_cursor(
    db: str, uuid: str, cursor: Union[Cursor, DictCursor]
) -> Union[tuple, dict]:
    """
    This function returns the record from the result of the "select by uuid" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    uuid: string
    This parameter specifies the uuid that will be used for this query

    cursor: Cursor
    This parameter is a pymysql.cursors that specifies
    which cursor will be used to execute the query

    return
    A dict containing the journal that matches with the upcoming uuid
    """
    params = __get_select_by_uuid_query(db, uuid)

    record = db_main.execute_single_record_select_with_cursor(cursor, params)

    return record


def commit(db: str, id_: str, region_name: str, secret_name: str) -> None:
    """
    This function commits a journal, which implies updating the state and post_date
    and then inserting it into QLDB

    db: string
    This parameter specifies the db name where the query will be executed

    id_: string
    This parameter specifies the uuid of the journal that will be commited

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials
    """
    import ark_qldb

    input_ = {
        "state": "POSTED",
        "postDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    params = __get_update_query(db, id_, input_, region_name, secret_name)
    query = params[0]
    q_params = params[1]

    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor(DictCursor)

    try:
        # Executing update of ledger first
        cursor.execute(query, q_params)

        # Then, inserting into QLDB
        journal_entry = select_by_uuid_with_cursor(db, id_, cursor)
        journal_entry["line_items"] = line_item.select_by_journal(
            db, journal_entry["id"], region_name, secret_name
        )
        journal_entry["attachments"] = attachment.select_by_journal(
            db, journal_entry["id"], region_name, secret_name
        )

        ark_qldb.post("journal_entry", dataclass_encoder.encode(journal_entry))

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

def __get_query_select_by_filter_paginated(db: str, filter: dict, limit: int, offset: int, sort: list) -> tuple:
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
    je.state, je.post_date, je.created_at, le.currency, le.decimals,
    fe.uuid as fund_entity_id,
    SUM(IF(li.posting_type="CREDIT", li.amount, 0)) as credits,
    SUM(IF(li.posting_type="DEBIT", li.amount, 0)) as debits

    FROM """
        + db
        + """.journal_entry je
    INNER JOIN """
        + db
        + """.ledger le ON (je.ledger_id = le.id)
    INNER JOIN """
        + db
        + """.line_item li ON (li.journal_entry_id = je.id)
    INNER JOIN """
        + db
        + """.account acc ON (li.account_id = acc.id)
    INNER JOIN """
        + db
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
        """
    )

    params = ()
    if filter:
        query += " WHERE 1=1 "
        for name, value in filter.items():
            if value is None:
                continue

            if name == "startDate":
                query += " AND je.date >= STR_TO_DATE(%s, '%%Y-%%m-%%d') "
            elif name == "endDate":
                query += " AND je.date <= STR_TO_DATE(%s, '%%Y-%%m-%%d') "
            elif name == "journalEntryState":
                query += " AND je.state = %s "
            elif name == "fundId":
                query += " AND fe.uuid = %s "
            elif name == "clientId":
                query += " AND fe.client_id = %s "
            elif name == "ledgerIds" and value:
                query += f' AND le.uuid IN ({",".join(["%s"] * len(value))}) '
                params += tuple(value)
                continue
            elif name == "entityIds" and value:
                if None in value:
                    query += f' AND (li.entity_id IS NULL '
                    non_null = [v for v in value if v is not None]
                    if non_null:
                        query += f' OR li.entity_id IN ({",".join(["%s"] * len(non_null))}) '
                        params += tuple(non_null)

                    query += ") "
                else:
                    query += f' AND li.entity_id IN ({",".join(["%s"] * len(value))}) '
                    params += tuple(value)

                continue
            elif name == "accountIds" and value:
                query += f' AND acc.uuid IN ({",".join(["%s"] * len(value))}) '
                params += tuple(value)
                continue
            elif name == "fundIds" and value:
                query += f' AND fe.uuid IN ({",".join(["%s"] * len(value))}) '
                params += tuple(value)
                continue
            elif name == "journalEntryIds" and value:
                query += f' AND je.uuid IN ({",".join(["%s"] * len(value))}) '
                params += tuple(value)
                continue
            else:
                continue

            params += (value,)

    query += " GROUP BY je.id "

    if sort:
        query += " ORDER BY "

        sort_list = []
        for item in sort:
            name = item["name"]
            desc = bool(item["descending"])

            if name == "fundId":
                sort_item = " fe.id "
            elif name == "ledgerName":
                sort_item = " le.name "
            elif name == "journalEntryNum":
                sort_item = " je.journal_entry_num "
            elif name == "date":
                sort_item = " je.date "
            elif name == "accountNo":
                sort_item = " CAST(acc.account_no as UNSIGNED) "
            elif name == "accountName":
                sort_item = " acc.name "
            elif name == "entityId":
                sort_item = " li.entity_id "
            elif name == "credits":
                sort_item = " credits "
            elif name == "debits":
                sort_item = " debits "
            elif name == "state":
                sort_item = " state "
            else:
                continue

            if desc:
                sort_item += " DESC "

            sort_list.append(sort_item)

        query += ",".join(sort_list)

    if limit:
        query += " LIMIT %s "
        params += (limit, )

    if offset:
        query += " OFFSET %s "
        params += (offset, )

    query += ";"
    return (query, params)


def __get_total_by_filter_query(db: str, filter: dict):

    query = (
        """SELECT COUNT(DISTINCT je.id) FROM """
        + db
        + """.journal_entry je
    INNER JOIN """
        + db
        + """.ledger le ON (je.ledger_id = le.id)
    INNER JOIN """
        + db
        + """.line_item li ON (li.journal_entry_id = je.id)
    INNER JOIN """
        + db
        + """.account acc ON (li.account_id = acc.id)
    INNER JOIN """
        + db
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
        """
    )

    params = ()
    if filter:
        query += " WHERE 1=1 "
        for name, value in filter.items():
            if value is None:
                continue

            if name == "startDate":
                query += " AND je.date >= STR_TO_DATE(%s, '%%Y-%%m-%%d') "
            elif name == "endDate":
                query += " AND je.date <= STR_TO_DATE(%s, '%%Y-%%m-%%d') "
            elif name == "journalEntryState":
                query += " AND je.state = %s "
            elif name == "fundId":
                query += " AND fe.uuid = %s "
            elif name == "clientId":
                query += " AND fe.client_id = %s "
            elif name == "ledgerIds" and value:
                query += f' AND le.uuid IN ({",".join(["%s"] * len(value))}) '
                params += tuple(value)
                continue
            elif name == "entityIds" and value:
                if None in value:
                    query += f' AND li.entity_id IS NULL '
                else:
                    query += f' AND li.entity_id IN ({",".join(["%s"] * len(value))}) '
                    params += tuple(value)
                continue
            elif name == "accountIds" and value:
                query += f' AND acc.uuid IN ({",".join(["%s"] * len(value))}) '
                params += tuple(value)
                continue
            elif name == "fundIds" and value:
                query += f' AND fe.uuid IN ({",".join(["%s"] * len(value))}) '
                params += tuple(value)
                continue
            elif name == "journalEntryIds" and value:
                query += f' AND je.uuid IN ({",".join(["%s"] * len(value))}) '
                params += tuple(value)
                continue
            else:
                continue

            params += (value,)
    return (query, params)


def select_with_filter_paginated(
    db: str,
    filter: dict,
    region_name: str,
    secret_name: str,
    page: int,
    page_size: int,
    sort: list = None
) -> list:
    """
    This function returns the record from the result of the "select by client id" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    filter: string
    A dict that contains all the possible filters:
        startDate: str
        endDate: str
        journalEntryState: str
        fundId: str
        clientId: str
        ledgerIds: list
        entityIds: list
        accountIds: list

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list containing the journal entries that match with the upcoming ledger_id
    """
    offset = None
    if page and page_size:
        offset = (page - 1) * page_size

    params = __get_query_select_by_filter_paginated(db, filter, page_size, offset, sort)

    print("QUERY PARAMS: ", params)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    total_params = __get_total_by_filter_query(db, filter)

    record = (
        db_main.execute_single_record_select(conn, total_params)
        or {"COUNT": 0}
    )

    total_records = list(record.values())[0]

    total_pages = 1
    if page_size is not None:
        total_pages = math.ceil(total_records / page_size)

    return (records, page, total_pages, total_records)


def select_numbers_by_ledger_uuid(
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
    params = __get_numbers_by_ledger_uuid_query(db, ledger_uuid)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return [record["journal_entry_num"] for record in records]


def __select_draft_accounts_and_ledgers_by_id_list_query(db: str, uuid_list: list):
    """
    Generate a query that will return draft-state ledgers and accounts
    related to a list of journal entry uuids
    """
    query = f"""
        SELECT l.uuid as ledger_id, l.state as ledger_state, a.uuid as account_id,
            a.state as account_state, je.uuid
        FROM {db}.line_item li

        INNER JOIN {db}.account a on a.id = li.account_id
        INNER JOIN {db}.journal_entry je on je.id = li.journal_entry_id
        INNER JOIN {db}.ledger l on l.id = je.ledger_id

        WHERE (a.state != "POSTED" or l.state != "POSTED")
            AND je.uuid in ({','.join(['%s'] * len(uuid_list))});"
        GROUP BY je.id;
    """

    params = tuple(uuid_list)
    return (query, params)

def select_draft_accounts_and_ledgers_by_id_list(db: str, uuid_list: list, region_name: str, secret_name: str):
    """
    This function returns a list of objects to represent DRAFT accounts or ledgers associated with a journal entry

    db: string
    This parameter specifies the db name where the query will be executed

    uuid_list: string
    A list of journal entry UUIDs

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list containing special objects to represent this case:
    [
        {
            ledger_id: ledger uuid,
            ledger_state: ["UNUSED", "DRAFT", "POSTED"]
            account_id: account uuid
            account_state: ["UNUSED", "DRAFT", "POSTED"]
            uuid: journal entry uuid
        }
    ]
    """

    params = __select_draft_accounts_and_ledgers_by_id_list_query(db, uuid_list)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def bulk_state(db: str, ledger_ids: list, region_name: str, secret_name: str) -> None:
    """
    This function updates the state and the post_date of a list of ledgers

    db: string
    This parameter specifies the db name where the query will be executed

    ledger_ids: list
    This parameter specifies the uuid list of the ledgers that will be commited

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials
    """

    input_ = {
        "state": "",
        "postDate": "",
    }
    params = __get_update_query(db, -1, input_, region_name, secret_name)
    state_query = params[0]

    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor(DictCursor)

    try:
        state_query_params = []
        post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for id_ in ledger_ids:
            state_query_params.append([
                "POSTED",
                post_date,
                id_
            ])

        cursor.executemany(state_query, state_query_params)

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()