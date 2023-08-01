"""
This Lambda is responsible for preforming the reconciliation process of Ledgers
"""

# pylint: disable=import-error; Lambda layer dependency
from ark_qldb import qldb
from arkdb import ledgers
from shared import logging, endpoint
import os
from amazon.ion.simple_types import IonPyNull

# pylint: enable=import-error

region_name = os.getenv("AWS_REGION")

@endpoint
def handler(
    event, context  # pylint: disable=unused-argument; Required lambda parameters
) -> tuple[int, dict]:
    """
    Lambda entry point

    event: object
    Event passed when the lambda is triggered

    context: object
    Lambda Context

    return: tuple[int, dict]
    Success code and an empty object
    """
    driver = qldb.Driver("ARKGL", region_name=region_name)
    buffered_cursor = driver.read_documents("ledger")
    processed_list = []
    processed_succesfully = []
    processed_failure = []

    for current_row in buffered_cursor:
        processed_success = True
        current_uuid = current_row["uuid"]

        aurora_record = ledgers.select_by_id(current_uuid, translate=False)
        if aurora_record is None:
            logging.write_log(
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
                if current_key not in aurora_record:
                    logging.write_log(
                        context,
                        "Error",
                        "Reconciliation error",
                        "Key " + str(current_key) + " does not exist in Aurora",
                    )
                    processed_success = False
                else:
                    if isinstance(current_row[current_key], IonPyNull):
                        current_key_value_qldb = str(None)
                    else:
                        current_key_value_qldb = str(current_row[current_key])

                    current_key_value_aurora = str(aurora_record[current_key])

                    if current_key_value_aurora != current_key_value_qldb:
                        logging.write_log(
                            context,
                            "Error",
                            "Reconciliation error",
                            "Error on value for key "
                            + current_key
                            + ". Key in QLDB: "
                            + current_key_value_qldb
                            + ". Key in Aurora: "
                            + current_key_value_aurora,
                        )
                        processed_success = False

        processed_list.append(current_row)
        if processed_success:
            processed_succesfully.append(current_row)
        else:
            processed_failure.append(current_row)

    ledger_count = ledgers.select_count_commited_ledgers()
    if ledger_count["count(*)"] != len(processed_list):
        logging.write_log(
            context,
            "Error",
            "Reconciliation error",
            "Error on amount of records on Aurora "
            + str(ledger_count["count(*)"])
            + " vs QLDB "
            + str(len(processed_list)),
        )

    if not processed_success:
        return 400, {}

    return 200, {}
