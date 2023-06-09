"""This module provides the Aurora MySQL serverless capabilities for getting reports"""

from datetime import datetime, timedelta
from . import db_main
from . import connection

def __get_query_with_common_params(select_query: str, input_: dict) -> tuple:
    """
    This function creates the report query's where clause using input parameters.

    select_query: string
    This parameter specifies the select query without filters, linked to the report

    input: dictionary
    This parameter contains all the common parameters inside a dictionary
    that will be used for the query:
    {
      "journalEntryState": "POSTED",
      "ledgerId": [
        "32fd629e-bc96-11ed-8a31-0ed8d524c7fe",
        "3fa85f64-5717-4562-b3fc-2c963f66afa6"
      ],
      "startDay": "2017-01-01",
      "endDay": "2017-05-31"
    }

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    where_clause = ""
    params = ()

    je_state = input_.get("journalEntryState")
    if je_state:
        where_clause += " AND je_state = %s "
        params += (je_state,)

    start_day = input_.get("startDay")
    if start_day:
        where_clause += " AND je_date >= STR_TO_DATE(%s, '%%Y-%%m-%%d %%T') "
        params += (start_day,)

    where_clause += " AND je_date < STR_TO_DATE(%s, '%%Y-%%m-%%d %%T') "

    end_day_input = input_.get("endDay")
    if end_day_input:
        end_day_dt = datetime.strptime(end_day_input, "%Y-%m-%d") + timedelta(days=1)
    else:
        end_day_dt = datetime.now() + timedelta(days=1)

    end_day = end_day_dt.strftime("%Y-%m-%d")

    params += (end_day,)

    ledgers_list = input_.get("ledgerId")

    format_strings = ",".join(["%s"] * len(ledgers_list))
    where_clause += f" AND le_uuid IN ({format_strings}) "

    params += tuple(ledgers_list)

    query = select_query + where_clause
    return (
        query,
        params,
    )


def select_trial_balance(
    db: str, input_: dict, region_name: str, secret_name: str
) -> dict:
    """
    This function returns the Trial Balance report.

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
    A list of dicts containing the Trial Balance report's data
    """
    select_query = (
        """
        SELECT *
        FROM """
        + db
        + """.TRIAL_BALANCE_VW
        WHERE 1=1 """
    )

    params = __get_query_with_common_params(select_query, input_)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def select_trial_balance_detail(
    db: str, input_: dict, region_name: str, secret_name: str
) -> dict:
    """
    This function returns the Detailed Trial Balance report.

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
    A list of dicts containing the Detailed Trial Balance report's data
    """
    select_query = (
        """
        SELECT *
        FROM """
        + db
        + """.DETAILED_TRIAL_BALANCE_VW
        WHERE 1=1 """
    )

    params = __get_query_with_common_params(select_query, input_)
    query = params[0]
    q_params = params[1]

    account_id = input_.get("accountId")
    if account_id:
        query += " AND acc_uuid = %s "
        q_params += (account_id,)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, (query, q_params))

    return records


def select_balance_sheet(
    db: str, input_: dict, region_name: str, secret_name: str
) -> dict:
    """
    This function returns the Balance Sheet report.

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
    A list of dicts containing the Balance Sheet report's data
    """
    select_query = (
        """
        SELECT *
        FROM """
        + db
        + """.BALANCE_SHEET_VW
        WHERE 1=1 """
    )

    params = __get_query_with_common_params(select_query, input_)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def select_income_statement(
    db: str, input_: dict, region_name: str, secret_name: str
) -> dict:
    """
    This function returns the Income Statement report.

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
    A list of dicts containing the Income Statement report's data
    """
    select_query = (
        """
        SELECT *
        FROM """
        + db
        + """.INCOME_STATEMENT_VW
        WHERE 1=1 """
    )

    params = __get_query_with_common_params(select_query, input_)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def select_1099(db: str, input_: dict, region_name: str, secret_name: str) -> dict:
    """
    This function returns the 1099 report.

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
    A list of dicts containing the 1099 report's data
    """
    select_query = (
        """
        SELECT *
        FROM """
        + db
        + """.1099_VW
        WHERE 1=1 """
    )

    params = __get_query_with_common_params(select_query, input_)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def select_1099_detail(
    db: str, input_: dict, region_name: str, secret_name: str
) -> dict:
    """
    This function returns the Detailed 1099 report.

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
    A list of dicts containing the Detailed 1099 report's data
    """
    select_query = (
        """
        SELECT *
        FROM """
        + db
        + """.DETAILED_1099_VW
        WHERE 1=1 """
    )

    params = __get_query_with_common_params(select_query, input_)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records


def select_1099_detail_balance(
    db: str, input_: dict, region_name: str, secret_name: str
) -> dict:
    """
    This function returns the Balance for Detailed 1099 report.

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
    A list of dicts containing the Balance for Detailed 1099 report's data
    """
    select_query = (
        """
        SELECT *
        FROM """
        + db
        + """.BALANCE_FOR_DETAILED_1099_VW
        WHERE 1=1 """
    )

    if "journalEntryState" in input_:
        del input_["journalEntryState"]

    params = __get_query_with_common_params(select_query, input_)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records
