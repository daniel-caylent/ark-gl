"""This module provides the Aurora MySQL serverless capabilities for ledgers"""
from . import db_main
from . import connection
from . import fund_entity

app_to_db = {
    "fundId": "fund_entity_id",
    "ledgerId": "uuid",
    "GLName": "name",
    "GLDescription": "description",
    "state": "state",
    "currencyName": "currency",
    "currencyDecimal": "`decimal`",
    "isHidden": "is_hidden",
}


def get_insert_query(db_: str, input_: dict, region_name: str, secret_name: str) -> tuple:
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
            (uuid, fund_entity_id, name, description, state, is_hidden, currency,  `decimal`)
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
        translated_input.get("`decimal`"),
    )

    return (query, params, uuid)


def get_update_query(db_: str, id_: str, input_: dict) -> tuple:
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


def get_delete_query(db_: str, id_: str) -> tuple:
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


def get_by_id(db_: str, id_: str) -> tuple:
    """
    This function creates the select by id query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id: string
    This parameter specifies the id that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = "SELECT * FROM " + db_ + ".ledger where uuid = %s;"

    params = (id_,)

    return (query, params)


def get_by_fund(db_: str, fund_id: str) -> tuple:
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
        SELECT le.*
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


def get_by_name(db_: str, ledger_name: str) -> tuple:
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
        SELECT *
        FROM """
        + db_
        + """.ledger
        where TRIM(LOWER(name)) = %s;"""
    )

    params = (ledger_name,)

    return (query, params)


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
    params = get_insert_query(db_, input_, region_name, secret_name)

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

    return
    A string specifying the recently added ledger's uuid
    """

    params = get_delete_query(db_, id_)

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

    return
    A string specifying the recently added ledger's uuid
    """
    params = get_update_query(db_, id_, input_)

    conn = connection.get_connection(db_, region_name, secret_name, db_type)

    query_list = [(params[0], params[1])]

    db_main.execute_dml(conn, query_list)
