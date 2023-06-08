"""
This Lambda is responsible for preforming the reconciliation process of Accounts
"""

# pylint: disable=import-error; Lambda layer dependency
from ark_qldb import qldb
from arkdb import accounts
from shared import endpoint, logging

# pylint: enable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]:
    """
    Lambda entry point

    event: object
    Event passed when the lambda is triggered

    context: object
    Lambda Context

    return: tuple[int, dict]
    Success code and an empty object
    """
    driver = qldb.Driver("ARKGL", region_name="us-east-1")
    buffered_cursor = driver.read_documents("account")
    processed_list = []
    processed_succesfully = []
    processed_failure = []

    for current_row in buffered_cursor:
        processed_success = True
        current_uuid = current_row["uuid"]

        aurora_record = accounts.select_by_id(current_uuid)
        if aurora_record is None:
            logging.write_log(
                event,
                context,
                "Error",
                "Reconciliation error",
                "Error on record "
                + str(aurora_record)
                + ".\nRecord exists in QLDB and not in Aurora",
            )
            processed_success = False
        else:
            for current_key in current_row.keys():
                if aurora_record.get(current_key) is None:
                    logging.write_log(
                        event,
                        context,
                        "Notice",
                        "Reconciliation Error",
                        "Key " + current_key + " does not exist in Aurora ",
                    )
                    processed_success = False
                else:
                    if aurora_record[current_key] != current_row[current_key]:
                        logging.write_log(
                            event,
                            context,
                            "Notice",
                            "Reconciliation Error",
                            "Error on value for key " + current_key,
                        )
                        processed_success = False

        processed_list.append(current_row)
        if processed_success:
            processed_succesfully.append(current_row)
        else:
            processed_failure.append(current_row)

    account_count = accounts.select_count_commited_accounts()
    if account_count["count(*)"] != len(processed_list):
        logging.write_log(
            event,
            context,
            "Notice",
            "Reconciliation Error",
            "Error on amount of records on Aurora "
            + str(account_count["count(*)"])
            + " vs QLDB "
            + str(len(processed_list)),
        )

    return 200, {}
