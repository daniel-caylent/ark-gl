"""
This Lambda is responsible for preforming the reconciliation process of JournalEntries
"""

# pylint: disable=import-error; Lambda layer dependency
from ark_qldb import qldb
from arkdb import journal_entries
from shared import logging

# pylint: enable=import-error


def __validate_journal_entry_key(
    event, context, aurora_record, current_key, current_row
):
    if aurora_record.get(current_key) is None:
        logging.write_log(
            event,
            context,
            "Error",
            "Reconciliation error",
            "Key " + current_key + " does not exist in Aurora ",
        )
        processed_success = False
    else:
        if aurora_record[current_key] != current_row[current_key]:
            logging.write_log(
                event,
                context,
                "Error",
                "Reconciliation error",
                "Error on value for key " + current_key,
            )
            processed_success = False
    return processed_success


def __validate_journal_entry_item(event, context, aurora_line_record, line_item):
    if aurora_line_record is None:
        logging.write_log(
            event,
            context,
            "Error",
            "Reconciliation error",
            "Error on record "
            + str(aurora_line_record)
            + ".\nRecord exists in QLDB and not in Aurora",
        )
        processed_success = False
    else:
        for line_current_key in line_item.keys():
            if line_current_key == "line_items":
                continue
            if aurora_line_record.get(line_current_key) is None:
                logging.write_log(
                    event,
                    context,
                    "Error",
                    "Reconciliation error",
                    "Key " + line_current_key + " does not exist in Aurora",
                )
                processed_success = False
            else:
                if aurora_line_record[line_current_key] != line_item[line_current_key]:
                    logging.write_log(
                        event,
                        context,
                        "Error",
                        "Reconciliation error",
                        "Error on value for key " + line_current_key,
                    )
                    processed_success = False
    return processed_success


# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
def __process_buffer(
    event,
    context,
    buffered_cursor,
    processed_list,
    processed_succesfully,
    processed_failure,
):
    for current_row in buffered_cursor:
        processed_success = True
        current_uuid = current_row["uuid"]

        aurora_record = journal_entries.select_by_id(current_uuid)
        if aurora_record is None:
            logging.write_log(
                event,
                context,
                "Error",
                "Reconciliation error",
                "Error on record "
                + str(aurora_record)
                + ".\nRecord does not exist in Aurora",
            )
            processed_success = False
        else:
            for current_key in current_row.keys():
                if current_key == "line_items":
                    continue
                processed_success = __validate_journal_entry_key(
                    event, context, aurora_record, current_key, current_row
                )

            current_row_id = current_row.get("id")
            qldb_line_records = current_row.get("line_items")

            for line_item in qldb_line_records:
                line_number = line_item.get("lineItemNo")
                aurora_line_record = journal_entries.select_line_by_number_journal(
                    line_number, current_row_id
                )
                processed_success = __validate_journal_entry_item(
                    event, context, aurora_line_record, line_item
                )

        processed_list.append(current_row)
        if processed_success:
            processed_succesfully.append(current_row)
        else:
            processed_failure.append(current_row)


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

    # Defining driver for qldb
    driver = qldb.Driver("ARKGL", region_name="us-east-1")

    # Reading from SQS queue
    for record in event["Records"]:
        journal_uuids = record["body"]

        buffered_cursor = driver.read_documents(
            "journal_entry", "uuid IN (" + journal_uuids.split(",") + ")"
        )
        processed_list = []
        processed_succesfully = []
        processed_failure = []

        __process_buffer(
            event,
            context,
            buffered_cursor,
            processed_list,
            processed_succesfully,
            processed_failure,
        )

        journal_count = journal_entries.select_count_commited_journals()
        if journal_count["count(*)"] != len(processed_list):
            logging.write_log(
                event,
                context,
                "Error",
                "Reconciliation error",
                "Error on amount of records on Aurora "
                + str(journal_count["count(*)"])
                + " vs QLDB "
                + str(len(processed_list)),
            )

    return 200, {}
