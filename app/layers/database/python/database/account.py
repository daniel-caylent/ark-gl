"""This module provides the Aurora MySQL serverless capabilities for accounts"""

from . import db_main
from . import connection
from . import account_attribute
from . import fund_entity
from . import fs
from pymysql.cursors import Cursor, DictCursor
from typing import Union

app_to_db = {
    "accountId": "uuid",
    "fundId": "fund_entity_id",
    "clientId": "client_id",
    "accountNo": "account_no",
    "state": "state",
    "parentAccountId": "parent_id",
    "accountName": "name",
    "accountDescription": "description",
    "attributeId": "account_attribute_id",
    "isHidden": "is_hidden",
    "isTaxable": "is_taxable",
    "isEntityRequired": "is_entity_required",
    "fsMappingId": "fs_mapping_id",
    "fsName": "fs_name",
    "isDryRun": "is_dry_run",
}


def __get_insert_query(
    db: str, input_: dict, fund_entity_id: str, region_name: str, secret_name: str
) -> tuple:
    """
    This function creates the insert query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    input_: dictionary
    This parameter contains all the parameters inside a dictionary that
    will be used for the query

    fund_entity_id: string
    This parameter specifies the fund_entity_id that will be used for this query

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
            state, is_hidden, is_taxable, is_entity_required, fs_mapping_id)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s);"""
    )

    translated_input = db_main.translate_to_db(app_to_db, input_)

    account_attribute_uuid = translated_input.get("account_attribute_id")
    account_attribute_id = account_attribute.get_id(
        db, account_attribute_uuid, region_name, secret_name
    )

    # Getting new uuid from the db to return it in insertion
    ro_conn = connection.get_connection(db, region_name, secret_name, "ro")
    uuid = db_main.get_new_uuid(ro_conn)

    # Evaluating if "parent_id" is null, to insert the uuid by default
    # if not, get the id from the parent's uuid
    parent_uuid = translated_input.get("parent_id")
    if parent_uuid:
        parent_id = get_id_by_uuid(db, parent_uuid, region_name, secret_name)
    else:
        parent_id = None

    # Evaluating if "fs_mapping_id" is null, to insert the uuid by default
    fs_mapping_id = translated_input.get("fs_mapping_id")

    params = (
        uuid,
        translated_input.get("account_no"),
        fund_entity_id,
        account_attribute_id,
        parent_id,
        translated_input.get("name"),
        translated_input.get("description"),
        translated_input.get("state"),
        translated_input.get("is_hidden"),
        translated_input.get("is_taxable"),
        translated_input.get("is_entity_required"),
        fs_mapping_id,
    )

    return (
        query,
        params,
        uuid,
        {"fs_mapping_id": fs_mapping_id, "fs_name": translated_input.get("fs_name")},
    )


def __get_update_query(
    db: str, id_: str, input_: dict, region_name: str, secret_name: str
) -> tuple:
    """
    This function creates the update query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id_: string
    This parameter specifies the uuid for identifying the account
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
        + """.account
        SET """
    )
    where_clause = "WHERE uuid = %s;"

    translated_input = db_main.translate_to_db(app_to_db, input_)

    if "fs_name" in translated_input:
        del translated_input["fs_name"]
    if "fs_mapping_id" in translated_input:
        del translated_input["fs_mapping_id"]
    if "client_id" in translated_input:
        del translated_input["client_id"]

    fund_entity_uuid = translated_input.get("fund_entity_id")
    if fund_entity_uuid:
        fund_entity_id = fund_entity.get_id(
            db, fund_entity_uuid, region_name, secret_name
        )
        translated_input["fund_entity_id"] = fund_entity_id

    account_attribute_uuid = translated_input.get("account_attribute_id")
    if account_attribute_uuid:
        account_attribute_id = account_attribute.get_id(
            db, account_attribute_uuid, region_name, secret_name
        )
        translated_input["account_attribute_id"] = account_attribute_id

    parent_uuid = translated_input.get("parent_id")
    if parent_uuid:
        parent_id = get_id_by_uuid(db, parent_uuid, region_name, secret_name)
        translated_input["parent_id"] = parent_id

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
        """
        SELECT acc.id, acc.account_no, acc.uuid,
        fe.uuid as fund_entity_id, attr.uuid as account_attribute_id, acc2.uuid as parent_id,
        acc.name, acc.description, fs.fs_mapping_id, fs.fs_name, acc.state, acc.is_hidden,
        acc.is_taxable, acc.is_entity_required, acc.created_at
        FROM """
        + db
        + """.account acc
        INNER JOIN """
        + db
        + """.fund_entity fe ON (acc.fund_entity_id = fe.id)
        inner join """
        + db
        + """.account_attribute attr on (acc.account_attribute_id = attr.id)
        left join """
        + db
        + """.account acc2 on (acc.parent_id = acc2.id)
        left join """
        + db
        + """.FS fs on (acc.fs_mapping_id = fs.fs_mapping_id)
        where acc.uuid = %s;"""
    )

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
        SELECT acc.id, acc.account_no, acc.uuid,
        fe.uuid as fund_entity_id, attr.uuid as account_attribute_id, acc2.uuid as parent_id,
        acc.name, acc.description, fs.fs_mapping_id, fs.fs_name, acc.state, acc.is_hidden,
        acc.is_taxable, acc.is_entity_required, acc.created_at
        FROM """
        + db
        + """.account acc
        INNER JOIN """
        + db
        + """.fund_entity fe ON (acc.fund_entity_id = fe.id)
        inner join """
        + db
        + """.account_attribute attr on (acc.account_attribute_id = attr.id)
        left join """
        + db
        + """.account acc2 on (acc.parent_id = acc2.id)
        left join """
        + db
        + """.FS fs on (acc.fs_mapping_id = fs.fs_mapping_id)
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
        + """.account
        where post_date IS NOT NULL;"""
    )

    params = ()

    return (query, params)


def __get_select_committed_between_dates_query(
    db: str, start_date: str, end_date: str
) -> tuple:
    """
    This function creates the select between dates for committed state accounts.

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
        + ".account where state = 'COMMITTED' and (post_date BETWEEN %s and %s);"
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
    A list of dicts containing the accounts that match with the upcoming dates
    """
    params = __get_select_committed_between_dates_query(db, start_date, end_date)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    record = db_main.execute_multiple_record_select(conn, params)

    return record


def check_fs(db: str, fs_mapping_id: str, region_name: str, secret_name: str) -> bool:
    """
    This function checks for the existence and validity of the upcoming FS

    db: string
    This parameter specifies the db name where the query will be executed

    fs_mapping_id: string
    This parameter specifies the fs_mapping_id that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A boolean indicating whether the FS should be inserted or not
    """

    # Checking if the upcoming fs_mapping_id exists
    fs_acc_check = select_by_uuid(db, fs_mapping_id, region_name, secret_name)

    if not fs_acc_check:
        raise Exception("The upcoming fsMappingId is invalid")

    # Checking if the FS row already exists, to insert or update later
    fs_check = fs.select_by_fs_mapping_id(db, fs_mapping_id, region_name, secret_name)

    insert_fs = bool(not fs_check)

    return insert_fs


def check_fs_with_cursor(
    db: str, fs_mapping_id: str, cursor: Union[Cursor, DictCursor]
) -> bool:
    """
    This function checks for the existence and validity of the upcoming FS

    db: string
    This parameter specifies the db name where the query will be executed

    fs_mapping_id: string
    This parameter specifies the fs_mapping_id that will be used for this query

    cursor: Cursor
    This parameter is a pymysql.cursors that specifies
    which cursor will be used to execute the query

    return
    A boolean indicating whether the FS should be inserted or not
    """

    # Checking if the upcoming fs_mapping_id exists
    fs_acc_check = select_by_uuid_with_cursor(db, fs_mapping_id, cursor)

    if not fs_acc_check:
        raise Exception("The upcoming fsMappingId is invalid")

    # Checking if the FS row already exists, to insert or update later
    fs_check = fs.select_by_fs_mapping_id_with_cursor(db, fs_mapping_id, cursor)

    insert_fs = bool(not fs_check)

    return insert_fs


def insert(db: str, input_: dict, region_name: str, secret_name: str) -> str:
    """
    This function executes the insert query with its parameters.

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
    A string specifying the recently added account's uuid
    """
    fund_dict = {
        "fund_entity_id": input_.get("fundId"),
        "client_id": input_.get("clientId"),
    }
    fund_entity_uuid = fund_dict["fund_entity_id"]
    if fund_entity_uuid:
        fund = fund_entity.select_by_uuid(
            db, fund_entity_uuid, region_name, secret_name
        )
    else:
        fund = None

    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor()

    try:
        # First of all, check if we have to insert fund_entity
        if fund:
            fund_entity_id = fund.get("id")
        else:
            fund_params = fund_entity.get_insert_query(db, fund_dict)

            cursor.execute(fund_params[0], fund_params[1])

            # Once inserted, get the auto-generated id
            fund_entity_id = cursor.lastrowid

        # Get insert query of account
        params = __get_insert_query(
            db, input_, fund_entity_id, region_name, secret_name
        )
        query = params[0]
        q_params = params[1]
        uuid = params[2]
        fs_dict = params[3]
        fs_mapping_id = fs_dict["fs_mapping_id"]
        fs_name = fs_dict["fs_name"]

        # Then, check if the FS has to be inserted
        if fs_mapping_id:
            insert_fs = check_fs(db, fs_mapping_id, region_name, secret_name)

        # After that, execute insert of account
        cursor.execute(query, q_params)

        # Then, inserting/updating FS
        if fs_mapping_id:
            if insert_fs:
                fs_params = fs.get_insert_query(db, fs_dict)
            else:
                fs_params = fs.get_update_query(db, fs_mapping_id, {"fs_name": fs_name})

            cursor.execute(fs_params[0], fs_params[1])

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

    return uuid


def delete(db: str, id_: str, region_name: str, secret_name: str) -> None:
    """
    This function executes the delete query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id_: string
    This parameter contains the uuid of the account that will be deleted

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
    params = __get_delete_query(db, id_)
    query = params[0]
    q_params = params[1]

    # Getting the fund_entity_id to check if we have to delete it
    account_ = select_by_uuid(db, id_, region_name, secret_name)
    fund_entity_uuid = account_.get("fund_entity_id")
    fund_entity_id = fund_entity.get_id(db, fund_entity_uuid, region_name, secret_name)

    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor()

    try:
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
        raise e
    finally:
        cursor.close()


def update(db: str, id_: str, input_: dict, region_name: str, secret_name: str) -> None:
    """
    This function executes the update query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    id_: string
    This parameter specifies the uuid of the account that will be updated

    input_: dictionary
    This parameter contains all the parameters inside a dictionary that
    will be used for the query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials
    """
    params = __get_update_query(db, id_, input_, region_name, secret_name)
    query = params[0]
    q_params = params[1]
    fs_mapping_id = input_.get("fsMappingId")
    fs_name = input_.get("fsName")
    fs_dict = {"fs_mapping_id": fs_mapping_id, "fs_name": fs_name}

    if fs_mapping_id:
        insert_fs = check_fs(db, fs_mapping_id, region_name, secret_name)

    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor()

    try:
        # Executing update of account first
        cursor.execute(query, q_params)

        # Then, inserting/updating FS
        if fs_mapping_id:
            if insert_fs:
                fs_params = fs.get_insert_query(db, fs_dict)
            else:
                fs_params = fs.get_update_query(db, fs_mapping_id, {"fs_name": fs_name})

            cursor.execute(fs_params[0], fs_params[1])

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()


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


def get_id_by_number(
    db: str, account_number: str, region_name: str, secret_name: str
) -> str:
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

    return record.get("id") if record else None


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
    A dict containing the account that matches with the upcoming uuid
    """
    params = __get_select_by_uuid_query(db, uuid)

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
    A dict containing the account that matches with the upcoming uuid
    """
    params = __get_select_by_uuid_query(db, uuid)

    record = db_main.execute_single_record_select_with_cursor(cursor, params)

    return record


def get_id_by_uuid(db: str, uuid: str, region_name: str, secret_name: str) -> str:
    """
    This function returns the id from an account with a specified account_number.

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
    A string representing the id of that Account record with uuid equals to the input
    """
    record = select_by_uuid(db, uuid, region_name, secret_name)

    return record.get("id") if record else None


def select_by_fund(db: str, fund_uuid: str, region_name: str, secret_name: str) -> list:
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


def __get_childs_by_ids_query(db: str, account_ids: list) -> tuple:
    """
    This function creates the select childs by ids query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_ids: list
    This parameter specifies the account_ids that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    format_strings = ",".join(["%s"] * len(account_ids))

    query = (
        """SELECT id
    FROM """
        + db
        + f".account where parent_id IN ({format_strings});"
    )

    params = tuple(account_ids)

    return (query, params)


def select_childs_by_ids(
    db: str, account_ids: list, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select childs by ids" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_ids: list
    This parameter specifies the account_ids that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list of dicts containing the child accounts that match with the upcoming account_ids
    """
    params = __get_childs_by_ids_query(db, account_ids)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def __get_uuid_by_ids_query(db: str, account_ids: list) -> tuple:
    """
    This function creates the select uuid by ids query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_ids: list
    This parameter specifies the account_ids that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    format_strings = ",".join(["%s"] * len(account_ids))

    query = (
        """SELECT uuid
    FROM """
        + db
        + f".account where id IN ({format_strings});"
    )

    params = tuple(account_ids)

    return (query, params)


def select_uuid_by_ids(
    db: str, account_ids: list, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select uuid by ids" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_ids: list
    This parameter specifies the account_ids that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list of uuids of the accounts that match with the upcoming account_ids
    """
    params = __get_uuid_by_ids_query(db, account_ids)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    records_uuids = [x.get("uuid") for x in records]

    return records_uuids


def __get_id_by_uuids_query(db: str, account_uuids: list) -> tuple:
    """
    This function creates the select uuid by ids query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_uuids: list
    This parameter specifies the account_uuids that will be used for this query

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    format_strings = ",".join(["%s"] * len(account_uuids))

    query = (
        """SELECT id
    FROM """
        + db
        + f".account where uuid IN ({format_strings});"
    )

    params = tuple(account_uuids)

    return (query, params)


def select_id_by_uuids(
    db: str, account_uuids: list, region_name: str, secret_name: str
) -> list:
    """
    This function returns the record from the result of the "select id by uuids" query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    account_uuids: list
    This parameter specifies the account_uuids that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list of ids of the accounts that match with the upcoming account_uuids
    """
    params = __get_id_by_uuids_query(db, account_uuids)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    records_ids = [x.get("id") for x in records]

    return records_ids


def get_recursive_childs_by_uuids(
    db: str, account_uuids: list, region_name: str, secret_name: str
) -> list:
    """
    This function returns the childs' and subchilds' ids
    from a list of parents' uuids.

    db: string
    This parameter specifies the db name where the query will be executed

    account_uuids: list
    This parameter specifies the account_uuids that will be used for this query

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A list of uuids of the child and subchild accounts that match with the upcoming parent account_uuids
    """
    childs_id_list = []

    # First of all, get the upcoming uuids and translate them to ids
    parent_ids = select_id_by_uuids(db, account_uuids, region_name, secret_name)

    # Getting first-level childs
    internal_child_list = select_childs_by_ids(db, parent_ids, region_name, secret_name)

    while len(internal_child_list) > 0:
        # Getting ids of the result (new parents) to iterate again
        new_parent_list = [x.get("id") for x in internal_child_list]

        # Appending result to main list
        childs_id_list += new_parent_list

        # Getting next level childs
        internal_child_list = select_childs_by_ids(
            db, new_parent_list, region_name, secret_name
        )

    # Getting uuids from child's and subchild's ids
    childs_uuid_list = select_uuid_by_ids(db, childs_id_list, region_name, secret_name)

    # Setting list to return (source uuids + childs and subchilds)
    # and removing duplicates
    result_list = account_uuids + childs_uuid_list
    result_list = list(dict.fromkeys(result_list))

    return result_list


def bulk_insert(db: str, input_list: list, region_name: str, secret_name: str) -> list:
    """
    This function executes the bulk insert query with its parameters.

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
    A list of strings specifying the recently added accounts' uuids
    """

    uuids_list = []

    conn = connection.get_connection(db, region_name, secret_name)
    cursor = conn.cursor(DictCursor)

    try:
        for input_ in input_list:
            fund_dict = {
                "fund_entity_id": input_.get("fundId"),
                "client_id": input_.get("clientId"),
            }
            fund_entity_uuid = fund_dict["fund_entity_id"]
            if fund_entity_uuid:
                fund = fund_entity.select_by_uuid_with_cursor(
                    db, fund_entity_uuid, cursor
                )
            else:
                fund = None

            # First of all, check if we have to insert fund_entity
            if fund:
                fund_entity_id = fund.get("id")
            else:
                fund_params = fund_entity.get_insert_query(db, fund_dict)

                cursor.execute(fund_params[0], fund_params[1])

                # Once inserted, get the auto-generated id
                fund_entity_id = cursor.lastrowid

            # Get insert query of account
            params = __get_insert_query(
                db, input_, fund_entity_id, region_name, secret_name
            )
            query = params[0]
            q_params = params[1]
            uuid = params[2]
            fs_dict = params[3]
            fs_mapping_id = fs_dict["fs_mapping_id"]
            fs_name = fs_dict["fs_name"]

            # Then, check if the FS has to be inserted
            if fs_mapping_id:
                insert_fs = check_fs_with_cursor(db, fs_mapping_id, cursor)

            # After that, execute insert of account
            cursor.execute(query, q_params)

            # Then, inserting/updating FS
            if fs_mapping_id:
                if insert_fs:
                    fs_params = fs.get_insert_query(db, fs_dict)
                else:
                    fs_params = fs.get_update_query(
                        db, fs_mapping_id, {"fs_name": fs_name}
                    )

                cursor.execute(fs_params[0], fs_params[1])

            uuids_list.append(uuid)

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

    return uuids_list
