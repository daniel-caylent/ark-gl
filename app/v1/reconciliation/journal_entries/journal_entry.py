"""
This Lambda is responsible for preforming the reconciliation process of JournalEntries
"""

# pylint: disable=import-error; Lambda layer dependency
from ark_qldb import qldb
from arkdb import journal_entries
from shared import logging, endpoint
import os
from amazon.ion.simple_types import IonPyNull

# pylint: enable=import-error

region_name = os.getenv("AWS_REGION")


def __validate_journal_entry_key(context, aurora_record, current_key, current_row):
    processed_success = True
    if current_key not in aurora_record:
        logging.write_log(
            context,
            "Error",
            "Reconciliation error",
            f"Key {current_key} does not exist in Aurora record: {aurora_record}",
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
    return processed_success


def __validate_journal_entry_subitem(context, aurora_record, qldb_record):
    processed_success = True
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
        for line_current_key in qldb_record.keys():
            if line_current_key == "line_items":
                continue
            if line_current_key not in aurora_record:
                logging.write_log(
                    context,
                    "Error",
                    "Reconciliation error",
                    "Key " + line_current_key + " does not exist in Aurora",
                )
                processed_success = False
            else:
                if isinstance(qldb_record[line_current_key], IonPyNull):
                    current_key_value_qldb = str(None)
                else:
                    current_key_value_qldb = str(qldb_record[line_current_key])

                current_key_value_aurora = str(aurora_record[line_current_key])

                if current_key_value_aurora != current_key_value_qldb:
                    logging.write_log(
                        context,
                        "Error",
                        "Reconciliation error",
                        "Error on value for key "
                        + line_current_key
                        + ". Key in QLDB: "
                        + current_key_value_qldb
                        + ". Key in Aurora: "
                        + current_key_value_aurora,
                    )
                    processed_success = False
    return processed_success


def __process_buffer(
    context,
    buffered_cursor,
    processed_list,
    processed_succesfully,
    processed_failure,
):
    processed_success = True
    for current_row in buffered_cursor:
        row_success = True
        current_uuid = current_row["uuid"]

        aurora_record = journal_entries.select_by_id(current_uuid, translate=False)

        if aurora_record is None:
            logging.write_log(
                context,
                "Error",
                "Reconciliation error",
                "Error on record "
                + str(aurora_record)
                + ".\nRecord does not exist in Aurora",
            )

            row_success = False
        else:
            for current_key in current_row.keys():
                if current_key in ["line_items", "attachments"]:
                    continue
                key_success = __validate_journal_entry_key(
                    context, aurora_record, current_key, current_row
                )
                
                if not key_success:
                    row_success = False

            current_row_id = current_row.get("id")
            qldb_line_records = current_row.get("line_items")
            qldb_attachments = current_row.get("attachments")

            for line_item in qldb_line_records:
                line_number = line_item.get("line_number")
                aurora_line_record = journal_entries.select_line_by_number_journal(
                    line_number, current_row_id
                )
                sub_item_success = __validate_journal_entry_subitem(
                    context, aurora_line_record, line_item
                )
                if not sub_item_success:
                    row_success = False

            for attachment in qldb_attachments:
                doc_id = attachment.get("uuid")
                aurora_att_record = journal_entries.select_attachment_by_uuid_journal(
                    doc_id, current_row_id
                )
                sub_item_success = __validate_journal_entry_subitem(
                    context, aurora_att_record, attachment
                )
                if not sub_item_success:
                    row_success = False

        processed_list.append(current_row)
        if row_success:
            processed_succesfully.append(current_row)
        else:
            processed_failure.append(current_row)
            processed_success = False
    return processed_success

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

    # Defining driver for qldb
    driver = qldb.Driver("ARKGL", region_name=region_name)

    # Reading from SQS queue
    for record in event["Records"]:
        journal_uuids = record["body"]

        buffered_cursor = driver.read_documents(
            "journal_entry", "uuid IN (" + (",").join(journal_uuids) + ")"
        )
        processed_list = []
        processed_succesfully = []
        processed_failure = []

        processed_success = __process_buffer(
            context,
            buffered_cursor,
            processed_list,
            processed_succesfully,
            processed_failure,
        )

        journal_count = journal_entries.select_count_commited_journals()
        if journal_count["count(*)"] != len(processed_list):
            logging.write_log(
                context,
                "Error",
                "Reconciliation error",
                "Error on amount of records on Aurora "
                + str(journal_count["count(*)"])
                + " vs QLDB "
                + str(len(processed_list)),
            )

            processed_success = False
    
    if not processed_success:
        return 400, {}
    return 200, {}
