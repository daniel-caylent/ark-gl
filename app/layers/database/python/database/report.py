"""This module provides the Aurora MySQL serverless capabilities for getting reports"""

from datetime import datetime, timedelta
from . import db_main
from . import connection
from . import account

app_to_db = {
    "fundId": "fund_uuid",
    "accountId": "account_uuid",
    "journalEntryNum": "journal_entry_num",
    "accountName": "account_name",
    "accountNo": "account_no",
    "displayName": "account_app_name",
    "attributeId": "attribute_uuid",
    "lineNumber": "line_number",
    "memo": "memo",
    "ledgerId": "ledger_uuid",
    "currency": "currency",
    "decimals": "decimals",
    "journalEntryPostDated": "journal_entry_post_date",
    "adjustingJournalEntry": "adjusting_journal_entry",
    "journalEntryState": "journal_entry_state",
    "journalEntryDate": "journal_entry_date",
    "amount": "amount",
    "entityId": "entity_id",
    "ledgerName": "ledger_name",
}

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

    for name, value in input_.items():
        if value is None:
            continue

        if name == "journalEntryState":
            where_clause += " AND journal_entry_state = %s "
        if name == "startDate":
            where_clause += " AND journal_entry_date >= STR_TO_DATE(%s, '%%Y-%%m-%%d') "
        if name == "endDate":
            where_clause += " AND journal_entry_date <= STR_TO_DATE(%s, '%%Y-%%m-%%d') "

        if name == "ledgerIds":
            format_strings = ",".join(["%s"] * len(value))
            where_clause += f" AND ledger_uuid IN ({format_strings}) "

            params += tuple(value)
            continue
        if name == "accountIds":
            format_strings = ",".join(["%s"] * len(value))
            where_clause += f" AND account_uuid IN ({format_strings}) "

            params += tuple(value)
            continue
        if name == "attributeIds":
            format_strings = ",".join(["%s"] * len(value))
            where_clause += f" AND attribute_uuid IN ({format_strings}) "

            params += tuple(value)
            continue

        params += (value,)
    query = select_query + where_clause
    return (
        query,
        params,
    )


def __get_account_tree_params(
    query_params: tuple, input_: dict, db: str, region_name: str, secret_name: str
) -> tuple:
    """
    This function creates the report query's where clause using accountId parameters.

    select_query: string
    This parameter specifies the select query without filters, linked to the report

    input: dictionary
    This parameter contains all the common parameters inside a dictionary
    that will be used for the query:
    {
      "accountId": [
        "534b95b9-0aa6-11ee-b49c-0a3efd619f29",
        "a9f912b2-f426-11ed-9a6e-0a3efd619f29"
        ]
    }

    return
    A tuple containing the query on the first element, and the params on the second
    one to avoid SQL Injections
    """
    query = query_params[0]
    q_params = query_params[1]

    account_id_list = input_.get("accountId")
    if account_id_list:
        acc_child_list = account.get_recursive_childs_by_uuids(
            db, account_id_list, region_name, secret_name
        )
        format_strings = ",".join(["%s"] * len(acc_child_list))
        query += f" AND acc_uuid IN ({format_strings}) "
        q_params += tuple(acc_child_list)

    return (query, q_params)


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

def get_start_balance_query(db, account_uuid, start_date):
    query = f"""
        SELECT SUM(CASE
			WHEN li.posting_type = 'CREDIT' then li.amount
			ELSE li.amount*(-1) END) as sum
        FROM {db}.line_item li
        INNER JOIN {db}.journal_entry je on je.id = li.journal_entry_id
        INNER JOIN {db}.account a on li.account_id = a.id
        WHERE a.uuid = %s and je.date < STR_TO_DATE(%s, '%%Y-%%m-%%d');
    """
    
    params = (account_uuid, start_date)

    return (query, params)

def select_start_balance(db: str, account_uuid: str, start_date: str, region_name: str, secret_name:str) -> int:
    if start_date is None:
        return 0

    query = get_start_balance_query(db, account_uuid, start_date)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    result = db_main.execute_single_record_select(conn, query)

    return list(result.values())[0]

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


def select_balance_sheet_detail(
    db: str, input_: dict, region_name: str, secret_name: str
) -> dict:
    """
    This function returns the Balance Sheet Detail report.

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
    A list of dicts containing the Balance Sheet Detail report's data
    """
    select_query = (
        """
        SELECT *
        FROM """
        + db
        + """.DETAILED_BALANCE_SHEET_VW
        WHERE 1=1 """
    )

    params = __get_query_with_common_params(select_query, input_)
    params = __get_account_tree_params(
        params, input_, db, region_name, secret_name)
    query = params[0]
    q_params = params[1]

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, (query, q_params))

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
