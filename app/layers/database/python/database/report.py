from datetime import datetime, timedelta

from . import db_main
from . import connection


def __get_trial_balance_query(db: str, input_: dict) -> tuple:
    """
    This function creates the Trial Balance report's query with its parameters.

    db: string
    This parameter specifies the db name where the query will be executed

    input: dictionary
    This parameter contains all the parameters inside a dictionary that
    will be used for the query:
    {
      "journalEntryState": "POSTED",
      "hideZeroBalance": true,
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
    select_query = (
        """
        SELECT *
        FROM """
        + db
        + """.TRIAL_BALANCE_VW
        WHERE 1=1 """
    )

    where_clause = ""
    params = ()

    je_state = input_.get("journalEntryState")
    if je_state:
        where_clause += " AND je_state = %s "
        params += (je_state,)

    if input_.get("hideZeroBalance"):
        where_clause += " AND DEBIT > 0 AND CREDIT > 0 "

    start_day = input_.get("startDay")
    if start_day:
        where_clause += " AND je_post_date >= STR_TO_DATE(%s, '%%Y-%%m-%%d %%T') "
        params += (start_day,)

    where_clause += " AND je_post_date < STR_TO_DATE(%s, '%%Y-%%m-%%d %%T') "

    end_day_input = input_.get("endDay")
    if end_day_input:
        end_day_dt = datetime.strptime(end_day_input, "%Y-%m-%d") + timedelta(days=1)
    else:
        end_day_dt = datetime.now() + timedelta(days=1)

    end_day = end_day_dt.strftime("%Y-%m-%d")

    params += (end_day,)

    ledgers_list = input_.get("ledgerId")

    format_strings = ",".join(["%s"] * len(ledgers_list))
    where_clause += f" AND le_uuid IN ({format_strings});"

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
    will be used for the query:
    {
      "journalEntryState": "POSTED",
      "hideZeroBalance": true,
      "ledgerId": [
        "32fd629e-bc96-11ed-8a31-0ed8d524c7fe",
        "3fa85f64-5717-4562-b3fc-2c963f66afa6"
      ],
      "startDay": "2017-01-01",
      "endDay": "2017-05-31"
    }

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A dict containing the Trial Balance report's data
    """
    params = __get_trial_balance_query(db, input_)

    conn = connection.get_connection(db, region_name, secret_name, "ro")

    records = db_main.execute_multiple_record_select(conn, params)

    return records
