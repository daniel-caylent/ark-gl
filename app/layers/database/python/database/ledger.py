"""This module provides the Aurora MySQL serverless capabilities for ledgers"""
from . import db_main
from . import connection
from . import fund_entity

app_to_db = {
    "fundId": "fund_entity_id",
    "ledgerId": "uuid",
    "glName": "name",
    "glDescription": "description",
    "state": "state",
    "currencyName": "currency",
    "currencyDecimal": "decimals",
    "isHidden": "is_hidden",
}


def __get_insert_query(
    db_: str, input_: dict, region_name: str, secret_name: str
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
            (uuid, fund_entity_id, name, description, state, is_hidden, currency,  decimals)
        VALUES
            (%s, %s, %s, %s, %s, %s,
            %s, %s);"""
    )

    translated_input = db_main.translate_to_db(app_to_db, input_)
    fund_entity_uuid = translated_input.get("fund_entity_id")
    fund_entity_id = fund_entity.get_id(db_, fund_entity_uuid, region_name, secret_name)
    # Getting new uuid from the db to return it in insertion
    ro_conn = connection.get_connection(db_, region_name, secret_name, "ro")
    uuid = db_main.get_new_uuid(ro_conn)

    params = (
        uuid,
        fund_entity_id,
        translated_input.get("name"),
        translated_input.get("description"),
        translated_input.get("state"),
        translated_input.get("is_hidden"),
        translated_input.get("currency"),
        translated_input.get("decimals"),
    )

    return (query, params, uuid)


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
                le.name, le.description, le.state, le.is_hidden,
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
                le.name, le.description, le.state, le.is_hidden,
                le.currency, le.decimals, le.created_at
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

    account_name: string
    This parameter specifies the account name

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    ledger_name = ledger_name.lower().strip()

    query = (
        """
        SELECT  le.id, le.uuid, fe.uuid as fund_entity_id,
                le.name, le.description, le.state, le.is_hidden,
                le.currency, le.decimals, le.created_at
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
                le.name, le.description, le.state, le.is_hidden,
                le.currency, le.decimals, le.created_at
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
        + ".ledger where state = 'COMMITTED' and (post_date BETWEEN %s and %s);"
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


def insert(
    db_: str, input_: dict, region_name: str, secret_name: str, db_type: str = None
) -> str:
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
    A string specifying the recently added ledger's uuid
    """
    params = __get_insert_query(db_, input_, region_name, secret_name)

    conn = connection.get_connection(db_, region_name, secret_name, db_type)
    query_params = [params[0], params[1]]
    uuid = params[2]
    query_list = [query_params]

    db_main.execute_dml(conn, query_list)

    return uuid


def delete(
    db_: str, id_: str, region_name: str, secret_name: str, db_type: str = None
) -> None:
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

    db_type: string (Optional)
    This parameter when set with 'ro' value is used to point the
    read only queries to a specific read only endpoint that will
    be optimized for this type of operations
    """

    params = __get_delete_query(db_, id_)

    conn = connection.get_connection(db_, region_name, secret_name, db_type)

    query_list = [(params[0], params[1])]

    db_main.execute_dml(conn, query_list)


def update(
    db_: str,
    id_: str,
    input_: dict,
    region_name: str,
    secret_name: str,
    db_type: str = None,
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

    db_type: string (Optional)
    This parameter when set with 'ro' value is used to point the
    read only queries to a specific read only endpoint that will
    be optimized for this type of operations
    """
    params = __get_update_query(db_, id_, input_)

    conn = connection.get_connection(db_, region_name, secret_name, db_type)

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
    This parameter specifies the ledger_name that will be used for this query

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
                le.name, le.description, le.state, le.is_hidden,
                le.currency, le.decimals, le.created_at
        FROM """
        + db
        + """.ledger le
        INNER JOIN """
        + db
        + """.fund_entity fe ON (le.fund_entity_id = fe.id)
        where le.uuid IN (%s);"""
        % format_strings
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
