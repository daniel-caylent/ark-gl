"""
This Lambda is responsible for preforming the reconciliation process of Ledgers
"""

from ark_qldb import qldb # pylint: disable=import-error; Lambda layer dependency
from arkdb import ledgers # pylint: disable=import-error; Lambda layer dependency


def handler(
    event, context # pylint: disable=unused-argument; Required lambda parameters
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
    driver = qldb.Driver("ARKGL", region_name="us-east-1")
    buffered_cursor = driver.read_documents("ledger")
    processed_list = []
    processed_succesfully = []
    processed_failure = []

    for current_row in buffered_cursor:
        processed_success = True
        current_uuid = current_row["uuid"]

        aurora_record = ledgers.select_by_id(current_uuid)
        if aurora_record is None:
            # TODO: add standard logging mechanism
            print(
                "Error"
            )  # record exists in QLDB and not in Aurora. Someone deleted it
            processed_success = False
        else:
            for current_key in current_row.keys():
                if aurora_record.get(current_key) is None:
                    # TODO: add standard logging mechanism
                    print(
                        "Key " + current_key + " does not exist in Aurora "
                    )  # key does not exist in Aurora
                    processed_success = False
                else:
                    if aurora_record[current_key] != current_row[current_key]:
                        # TODO: add standard logging mechanism
                        print(
                            "Error on value for key " + current_key
                        )  # record value mistmatch. Someone tampered with the DB
                        processed_success = False

        processed_list.append(current_row)
        if processed_success:
            processed_succesfully.append(current_row)
        else:
            processed_failure.append(current_row)

    ledger_count = ledgers.select_count_commited_ledgers()
    if ledger_count["count(*)"] != len(processed_list):
        # TODO: add standard logging mechanism
        print(
            "Error on amount of records on Aurora "
            + str(ledger_count["count(*)"])
            + " vs QLDB "
            + str(len(processed_list))
        )  # distinct amount of ledgers in the QLDB than the DB

    return 200, {} #
