"""
This Lambda is responsible for preforming the reconciliation process of Accounts
"""

# pylint: disable=import-error; Lambda layer dependency
from ark_qldb import qldb
from arkdb import accounts
from shared import logging
from hashlib import sha256
import os
from amazon.ion.simple_types import IonPyNull

# pylint: enable=import-error

region_name = os.getenv("AWS_REGION")
HASH_NAMES = ["memo", "reference"]
IGNORE_NAMES = ["fs_name", "fs_mapping_id", "is_taxable", "is_entity_required"]

@logging.use_logging
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
    buffered_cursor = driver.read_documents("account")
    processed_list = []
    processed_succesfully = []
    processed_failure = []
    fail_uuids = []

    for current_row in buffered_cursor:
        current_uuid = current_row["uuid"]
        fail_reasons = []

        aurora_record = accounts.select_by_id(current_uuid, translate=False)
        if aurora_record is None:
            fail_reason = f"Error on record {current_uuid}. Record exists in QLDB and not in Aurora",
            logging.write_log(
                context,
                "Error",
                "Reconciliation error",
                fail_reason
            )

            fail_reasons.append(fail_reason)

        else:
            for current_key in current_row.keys():
                if current_key in IGNORE_NAMES:
                    continue

                if current_key not in aurora_record:
                    fail_reason = f"Key '{current_key}' for uuid: '{current_uuid}' does not exist in Aurora"
                    logging.write_log(
                        context,
                        "Notice",
                        "Reconciliation Error",
                        fail_reason,
                    )
                    fail_reasons.append(fail_reason)
                else:
                    if isinstance(current_row[current_key], IonPyNull):
                        current_key_value_qldb = str(None)
                    else:
                        current_key_value_qldb = str(current_row[current_key])

                    if current_key in HASH_NAMES:
                        current_key_value_aurora = str(
                            sha256(
                                aurora_record[current_key].encode("utf-8")
                            ).hexdigest()
                        )
                    else:
                        current_key_value_aurora = str(aurora_record[current_key])

                    if current_key_value_aurora != current_key_value_qldb:
                        fail_reason = f"Error on value for key '{current_key}' for uuid: '{current_uuid}'. Value in QLDB: {current_key_value_qldb}. Value in Aurora: {current_key_value_aurora}"
                        logging.write_log(
                            context,
                            "Error",
                            "Reconciliation error",
                            fail_reason,
                        )
                        fail_reasons.append(fail_reason)

        processed_list.append(current_row)
        if fail_reasons:
            processed_failure.append({
                "error_on": current_uuid,
                "detail": fail_reasons
            })
            fail_uuids.append(current_uuid)
        else:
            processed_succesfully.append(current_uuid)

    account_count = accounts.select_count_commited_accounts()
    if account_count["count(*)"] != len(processed_list):
        fail_reason = f"Error on amount of records on Aurora {account_count['count(*)']} vs QLDB {len(processed_list)}"
        logging.write_log(
            context,
            "Error",
            "Reconciliation error",
            fail_reason
        )

        processed_failure.append(
            {
                "error_on": "count(*)",
                "detail": fail_reason
            }
        )

    status = 200
    if processed_failure:
        status = 400

    return status, {
        "fail_count": len(set(fail_uuids)),
        "success_count": len(processed_succesfully)
    }
