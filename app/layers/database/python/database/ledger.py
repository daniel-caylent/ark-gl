"""This module provides the Aurora MySQL serverless capabilities for ledgers"""

from . import db_main
from . import connection
from . import fund_entity
from pymysql.cursors import Cursor, DictCursor
from typing import Union
from datetime import datetime
from shared import dataclass_encoder

app_to_db = {
    "fundId": "fund_entity_id",
    "clientId": "client_id",
    "ledgerId": "uuid",
    "glName": "name",
    "glDescription": "description",
    "state": "state",
    "currencyName": "currency",
    "currencyDecimal": "decimals",
    "postDate": "post_date",
}


def __get_insert_query(
    db_: str, input_: dict, fund_entity_id: str, region_name: str, secret_name: str
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
        + db_
        + """.ledger
            (uuid, fund_entity_id, name, description, state, currency,  decimals)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s);"""
    )

    translated_input = db_main.translate_to_db(app_to_db, input_)

    # Getting new uuid from the db to return it in insertion
    uuid = db_main.get_new_uuid()

    params = (
        uuid,
        fund_entity_id,
        translated_input.get("name"),
        translated_input.get("description"),
        translated_input.get("state"),
        translated_input.get("currency"),
        translated_input.get("decimals"),
    )

    return (
        query,
        params,
        uuid,
    )


def __get_update_query(db_: str, id_: str, input_: dict) -> tuple:
    """
    This function creates the update query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id: string
    This parameter specifies the uuid for identifying the ledger
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
        + db_
        + """.ledger
        SET """
    )
    where_clause = "WHERE uuid = %s;"

    translated_input = db_main.translate_to_db(app_to_db, input_)

    if "client_id" in translated_input:
        del translated_input["client_id"]

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


def __get_delete_query(db_: str, id_: str) -> tuple:
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
        + db_
        + """.ledger
        WHERE uuid = %s;"""
    )

    params = (id_,)

    return (query, params)


def __get_by_uuid_query(db: str, uuid: str) -> tuple:
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
        """
        SELECT  le.id, le.uuid, fe.uuid as fund_entity_id,
                le.name, le.description, le.post_date, le.state,
                le.currency, le.decimals, le.created_at
        FROM """
        + db
        + """.ledger le
        INNER JOIN """
        + db
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
        where le.uuid = %s;"""
    )

    params = (uuid,)

    return (query, params)


def __get_by_fund_query(db_: str, fund_id: str) -> tuple:
    """
    This function creates the select by fund id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    fund_id: string
    This parameter specifies the fund uuid that will be used for the select in the query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """
        SELECT  le.id, le.uuid, fe.uuid as fund_entity_id,
                le.name, le.description, le.state,
                le.currency, le.decimals, le.created_at, le.post_date
        FROM """
        + db_
        + """.ledger le
        INNER JOIN """
        + db_
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
        where fe.uuid = %s;"""
    )

    params = (fund_id,)

    return (query, params)


def __get_by_name_query(db_: str, ledger_name: str) -> tuple:
    """
    This function creates the select by name query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    ledger_name: string
    This parameter specifies the ledger name that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    ledger_name = ledger_name.lower().strip()

    query = (
        """
        SELECT  le.id, le.uuid, fe.uuid as fund_entity_id,
                le.name, le.description, le.state,
                le.currency, le.decimals, le.created_at, le.post_date
        FROM """
        + db_
        + """.ledger le
        INNER JOIN """
        + db_
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
        where TRIM(LOWER(le.name)) = %s;"""
    )

    params = (ledger_name,)

    return (query, params)


def __get_by_client_id_query(db_: str, client_id: str) -> tuple:
    """
    This function creates the select by client_id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    client_id: string
    This parameter specifies the client_id that will be used for the select in the query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """
        SELECT  le.id, le.uuid, fe.uuid as fund_entity_id,
                le.name, le.description, le.state,
                le.currency, le.decimals, le.created_at, le.post_date
        FROM """
        + db_
        + """.ledger le
        INNER JOIN """
        + db_
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
        where fe.client_id = %s;"""
    )

    params = (client_id,)

    return (query, params)


def __get_select_committed_between_dates_query(
    db: str, start_date: str, end_date: str
) -> tuple:
    """
    This function creates the select between dates for committed state ledgers.

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
        + ".ledger where state = 'POSTED' and (post_date BETWEEN %s and %s);"
    )

    params = (
        start_date,
        end_date,
    )

    return (query, params)


def select_committed_between_dates(
    db: str, start_date: str, end_date: str, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select commited between dates" query with its parameters.

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
    A list of dicts containing the ledgers that match with the upcoming dates
    """
    params = __get_select_committed_between_dates_query(db, start_date, end_date)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_multiple_record_select(conn, params)

    return record


def insert(db_: str, input_: dict, region_name: str, secret_name: str) -> str:
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

    return
    A string specifying the recently added ledger's uuid
    """
    fund_dict = {
        "fund_entity_id": input_.get("fundId"),
        "client_id": input_.get("clientId"),
    }
    fund_entity_uuid = fund_dict["fund_entity_id"]
    if fund_entity_uuid:
        fund = fund_entity.select_by_uuid(
            db_, fund_entity_uuid, region_name, secret_name
        )
    else:
        fund = None

    conn = connection.get_connection(db_, region_name, secret_name)
    cursor = conn.cursor()

    try:
        # First of all, check if we have to insert fund_entity
        if fund:
            fund_entity_id = fund.get("id")
        else:
            fund_params = fund_entity.get_insert_query(db_, fund_dict)

            cursor.execute(fund_params[0], fund_params[1])

            # Once inserted, get the auto-generated id
            fund_entity_id = cursor.lastrowid

        # Get insert query of ledger
        params = __get_insert_query(
            db_, input_, fund_entity_id, region_name, secret_name
        )
        query = params[0]
        q_params = params[1]
        uuid = params[2]

        # After that, execute insert of ledger
        cursor.execute(query, q_params)

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

    return uuid


def delete(db_: str, id_: str, region_name: str, secret_name: str) -> None:
    """
    This function executes the delete query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id: string
    This parameter contains the uuid of the ledger that will be deleted

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials
    """

    params = __get_delete_query(db_, id_)
    query = params[0]
    q_params = params[1]

    # Getting the fund_entity_id to check if we have to delete it
    ledger_ = select_by_uuid(db_, id_, region_name, secret_name)
    fund_entity_uuid = ledger_.get("fund_entity_id")
    fund_entity_id = fund_entity.get_id(db_, fund_entity_uuid, region_name, secret_name)

    conn = connection.get_connection(db_, region_name, secret_name)
    cursor = conn.cursor(DictCursor)

    try:
        # Executing delete of ledger first
        cursor.execute(query, q_params)

        # Then, checking if the fund was orphaned
        fund_count = fund_entity.get_accounts_ledgers_count(db_, fund_entity_id, cursor)

        if fund_count == 0:
            fund_params = fund_entity.get_delete_query_by_id(db_, fund_entity_id)

            cursor.execute(fund_params[0], fund_params[1])

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()


def update(
    db_: str,
    id_: str,
    input_: dict,
    region_name: str,
    secret_name: str,
) -> None:
    """
    This function executes the update query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id: string
    This parameter specifies the uuid of the ledger that will be updated

    input: dictionary
    This parameter contains all the parameters inside a dictionary that
    will be used for the query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials
    """
    params = __get_update_query(db_, id_, input_)

    conn = connection.get_connection(db_, region_name, secret_name)

    query_list = [(params[0], params[1])]

    db_main.execute_dml(conn, query_list)


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
    A dict containing the ledger that matches with the upcoming uuid
    """
    params = __get_by_uuid_query(db, uuid)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_single_record_select(conn, params)

    return record


def select_by_fund(db: str, fund_id: str, region_name: str, secret_name: str) -> list:
    """
    This function returns the record from the result of the "select by fund" query with its parameters.

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
    A list of dicts containing the ledgers that match with the upcoming fund_id
    """
    params = __get_by_fund_query(db, fund_id)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def select_by_name(
    db: str, ledger_name: str, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select by fund" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    ledger_name: string
    This parameter specifies the ledger name that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list of dicts containing the ledgers that match with the upcoming ledger_name
    """
    params = __get_by_name_query(db, ledger_name)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def select_by_client_id(
    db: str, client_id: str, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select by client" query with its parameters.

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
    A list of dicts containing the ledgers that match with the upcoming fund_id
    """
    params = __get_by_client_id_query(db, client_id)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def get_id(db: str, uuid: str, region_name: str, secret_name: str) -> str:
    """
    This function returns the id from a ledger with a specified uuid.

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
    A string representing the id of that Ledger record with uuid equals to the input
    """
    record = select_by_uuid(db, uuid, region_name, secret_name)

    return record.get("id")


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
        + """.ledger
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


def __get_by_multiple_uuids_query(db: str, uuids_list: list) -> tuple:
    """
    This function creates the select by multiple uuids query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    uuids_list: list
    This parameter specifies the list of uuids that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    format_strings = ",".join(["%s"] * len(uuids_list))

    query = (
        """
        SELECT  le.id, le.uuid, fe.uuid as fund_entity_id,
                le.name, le.description, le.state,
                le.currency, le.decimals, le.created_at, le.post_date
        FROM """
        + db
        + """.ledger le
        INNER JOIN """
        + db
        + f".fund_entity fe ON (le.fund_entity_id = fe.id) WHERE le.uuid IN ({format_strings});"
    )

    params = tuple(uuids_list)

    return (query, params)


def select_by_multiple_uuids(
    db: str, uuids_list: list, region_name: str, secret_name: str
) -> dict:
    """
    This function returns the record from the result of the "select by multiple uuids" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    uuids_list: list
    This parameter specifies the list of uuids that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A dict containing the ledgers that match with the upcoming uuids
    """
    params = __get_by_multiple_uuids_query(db, uuids_list)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def __get_by_fund_and_name_query(db_: str, fund_uuid: str, ledger_name: str) -> tuple:
    """
    This function creates the select by fund uuid and ledger name query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    fund_uuid: string
    This parameter specifies the fund's uuid that will be used for this query

    ledger_name: string
    This parameter specifies the ledger name that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    ledger_name = ledger_name.lower().strip()

    query = (
        """
        SELECT  le.id, le.uuid, fe.uuid as fund_entity_id,
                le.name, le.description, le.state,
                le.currency, le.decimals, le.created_at, le.post_date
        FROM """
        + db_
        + """.ledger le
        INNER JOIN """
        + db_
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
        where TRIM(LOWER(le.name)) = %s and fe.uuid = %s;"""
    )

    params = (ledger_name, fund_uuid)

    return (query, params)


def select_by_fund_and_name(
    db: str, fund_uuid: str, ledger_name: str, region_name: str, secret_name: str
) -> dict:
    """
    This function returns the record from the result of the "select by fund and name" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    fund_uuid: string
    This parameter specifies the fund's uuid that will be used for this query

    ledger_name: string
    This parameter specifies the ledger name that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A dict containing the ledger that matches with the upcoming ledger_name and fund_uuid
    """
    params = __get_by_fund_and_name_query(db, fund_uuid, ledger_name)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_single_record_select(conn, params)

    return record


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
    A dict containing the ledger that matches with the upcoming uuid
    """
    params = __get_by_uuid_query(db, uuid)

    record = db_main.execute_single_record_select_with_cursor(cursor, params)

    return record


def commit(db: str, id_: str, region_name: str, secret_name: str) -> None:
    """
    This function commits a ledger, which implies updating the state and post_date
    and then inserting it into QLDB

    db: string
    This parameter specifies the db name where the query will be executed

    id_: string
    This parameter specifies the uuid of the ledger that will be commited

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
    params = __get_update_query(db, id_, input_)
    query = params[0]
    q_params = params[1]

    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor(DictCursor)

    try:
        # Executing update of ledger first
        cursor.execute(query, q_params)

        # Then, inserting into QLDB
        ledger_ = select_by_uuid_with_cursor(db, id_, cursor)
        ark_qldb.post("ledger", dataclass_encoder.encode(ledger_))

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

def bulk_delete(db: str, ids: list, region_name: str, secret_name: str) -> None:
    """
    This function executes the delete query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    ids: list
    A list of IDs which should all be deleted

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials
    """


    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor(DictCursor)

    try:
        for id_ in ids:
            params = __get_delete_query(db, id_)
            query = params[0]
            q_params = params[1]

            # Getting the fund_entity_id to check if we have to delete it
            ledger = select_by_uuid(db, id_, region_name, secret_name)
            fund_entity_uuid = ledger.get("fund_entity_id")
            fund_entity_id = fund_entity.get_id(db, fund_entity_uuid, region_name, secret_name)

            # Executing delete of account first
            cursor.execute(query, q_params)

            # Then, checking if the fund was orphaned
            fund_count = fund_entity.get_accounts_ledgers_count(db, fund_entity_id, cursor)

            if fund_count == 0:
                fund_params = fund_entity.get_delete_query_by_id(db, fund_entity_id)

                cursor.execute(fund_params[0], fund_params[1])

            conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Unable to delete ledger: {id_}")


def bulk_state(db: str, ledger_ids: list, post_date: str, region_name: str, secret_name: str) -> None:
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
    params = __get_update_query(db, -1, input_)
    state_query = params[0]

    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor(DictCursor)

    try:
        state_query_params = []
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
