"""This module provides the Aurora MySQL serverless capabilities for accounts"""
from . import db_main
from . import connection
from . import account_attribute
from . import fund_entity

app_to_db = {
    'accountId': "uuid",
    'fundId': "fund_entity_id",
    'accountNo': "account_no",
    'state': "state",
    'parentAccountNo': "parent_id",
    'accountName': "name",
    'accountDescription': "description",
    'attributeNo': "account_attribute_no",
    'isHidden': "is_hidden",
    'isTaxable': "is_taxable",
    'isVendorCustomerPartnerRequired': "is_vendor_customer_partner_required",
    'FSMappingId': "fs_mapping_id",
    'FSName': "fs_name",
    'isDryRun': "is_dry_run"
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
        + """.account
            (uuid, account_no, fund_entity_id, account_attribute_id, parent_id, name, description,
            state, is_hidden, is_taxable, is_vendor_customer_partner_required)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s);"""
    )

    translated_input = db_main.translate_to_db(app_to_db, input)

    fund_entity_uuid = translated_input.get("fund_entity_id")
    fund_entity_id = fund_entity.get_id(db, fund_entity_uuid, region_name, secret_name)
    account_attribute_uuid = translated_input.get("account_attribute_id")
    account_attribute_id = account_attribute.get_id(
        db, account_attribute_uuid, region_name, secret_name
    )

    # Getting new uuid from the db to return it in insertion
    ro_conn = connection.get_connection(db, region_name, secret_name, "ro")
    uuid = db_main.get_new_uuid(ro_conn)

    params = (
        uuid,
        translated_input.get("account_no"),
        fund_entity_id,
        account_attribute_id,
        translated_input.get("parent_id"),
        translated_input.get("name"),
        translated_input.get("description"),
        translated_input.get("state"),
        translated_input.get("is_hidden"),
        translated_input.get("is_taxable"),
        translated_input.get("is_vendor_customer_partner_required"),
    )

    return (query, params, uuid)


def __get_update_query(db: str, id: str, input: dict) -> tuple:
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
        + db
        + """.account
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
        + """.account
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
    query = "SELECT * FROM " + db + ".account where uuid = %s;"

    params = (uuid,)

    return (query, params)


def __get_select_by_fund_query(db: str, fund_id: str) -> tuple:
    """
    This function creates the select by fund_entity uuid query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    fund_id: string
    This parameter specifies the fund_entity uuid that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = (
        """
        SELECT acc.*
        FROM """
        + db
        + """.account acc
        INNER JOIN """
        + db
        + """.fund_entity fe ON (acc.fund_entity_id = fe.id)
        where fe.uuid = %s;"""
    )

    params = (fund_id,)

    return (query, params)


def __get_select_by_name_query(db: str, account_name: str) -> tuple:
    """
    This function creates the select by name query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_name: string
    This parameter specifies the account_name that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    account_name = account_name.lower().strip()
    query = (
        """
        SELECT *
        FROM """
        + db
        + """.account
        where TRIM(LOWER(name)) = %s;"""
    )

    params = (account_name,)

    return (query, params)


def insert(db: str, input: dict, region_name: str, secret_name: str) -> str:
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
    A string specifying the recently added account's uuid
    """
    params = __get_insert_query(db, input, region_name, secret_name)

    query_params = [params[0], params[1]]
    uuid = params[2]

    conn = connection.get_connection(db, region_name, secret_name)

    query_list = [query_params]

    db_main.execute_dml(conn, query_list)

    return uuid


def delete(db: str, id: str, region_name: str, secret_name: str) -> None:
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
    params = __get_delete_query(db, id)

    conn = connection.get_connection(db, region_name, secret_name)

    query_list = [(params[0], params[1])]

    db_main.execute_dml(conn, query_list)


def update(db: str, id: str, input: dict, region_name: str, secret_name: str) -> None:
    """
    This function executes the update query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id: string
    This parameter specifies the uuid of the account that will be updated

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
    params = __get_update_query(db, id, input)

    conn = connection.get_connection(db, region_name, secret_name)

    query_list = [(params[0], params[1])]

    db_main.execute_dml(conn, query_list)


def __get_by_number_query(db: str, account_number: str) -> tuple:
    """
    This function creates the select by account_no query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_number: string
    This parameter specifies the account_number that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = "SELECT * FROM " + db + ".account where account_no = %s;"

    params = (account_number,)

    return (query, params)


def select_by_number(
    db: str, account_number: str, region_name: str, secret_name: str
) -> dict:
    """
    This function returns the record from the result of the "select by number" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_number: string
    This parameter specifies the account_number that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A dict containing the account that matches with the upcoming account_number
    """
    params = __get_by_number_query(db, account_number)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_single_record_select(conn, params)

    return record


def get_id(db: str, account_number: str, region_name: str, secret_name: str) -> str:
    """
    This function returns the id from an account with a specified account_number.

    db: string
    This parameter specifies the db name where the query will be executed

    account_number: string
    This parameter specifies the account_number that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A string representing the id of that Account record with account_no equals to the input
    """
    record = select_by_number(db, account_number, region_name, secret_name)

    return record.get("id")


def select_by_uuid(
    db: str, uuid: str, region_name: str, secret_name: str
) -> dict:
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
    A dict containing the account that matches with the upcoming uuid
    """
    params = __get_select_by_uuid_query(db, uuid)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_single_record_select(conn, params)

    return record


def select_by_fund(
    db: str, fund_uuid: str, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select by fund" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    fund_id: string
    This parameter specifies the fund_entity's uuid that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list of dicts containing the accounts that match with the upcoming fund's uuid
    """
    params = __get_select_by_fund_query(db, fund_uuid)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_multiple_record_select(conn, params)

    return record


def select_by_name(
    db: str, account_name: str, region_name: str, secret_name: str
) -> dict:
    """
    This function returns the record from the result of the "select by name" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_name: string
    This parameter specifies the account_name that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A dict containing the account that matches with the upcoming name
    """
    params = __get_select_by_name_query(db, account_name)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_single_record_select(conn, params)

    return record
