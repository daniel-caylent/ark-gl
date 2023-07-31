"""Lambda that will perform PUT requests for Journal Entries / state"""
import os
import json
import boto3

# pylint: disable=import-error; Lambda layer dependency
from arkdb import journal_entries
from shared import (
    endpoint,
    validate_uuid,
    logging,
    filtering,
    dataclass_error_to_str
)
from journal_entries_shared import utils as je_utils
from models import JournalEntry
# pylint: enable=import-error

sqs = boto3.client('sqs')
s3 = boto3.client('s3')


def __validate_journal_entries(journal_entry_ids: []):
    journal_entry_objects = []

    for id_ in journal_entry_ids:
        if not validate_uuid(id_):
            return 400, {"detail": f"Invalid uuid: {id_}"}

        result = journal_entries.select_by_id(id_, False)
        if result is None:
            return 404, {"detail": f"No journal entry found for: {id_}"}

        if result["state"] == "POSTED":
            return 400, {"detail": f"POSTED journal entry cannot be posted: {id_}"}

        journal_entry_objects.append(result)

    return journal_entry_objects


def __save_to_s3(chunks, bucket_name, prefix):
    s3_filenames = []
    for index, chunk in enumerate(chunks):
        filename = f"{prefix}_chunk_{index}.json"
        s3_path = f"{prefix}/{filename}"

        # Convert the chunk to JSON
        chunk_json = json.dumps(chunk)

        # Upload the chunk to S3
        s3_client.put_object(Bucket=bucket_name, Key=s3_path, Body=chunk_json)

        # Add the filename to the list
        s3_filenames.append(f"s3://{bucket_name}/{s3_path}")


@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters

    # validate the request body
    try:
        body = json.loads(event["body"])
    except Exception:
        return 400, {"detail": "Body does not contain valid json."}

    try:
        valid_input = filtering.FilterInput(**body).get_dict()
    except Exception as e:
        return 400, {"detail": dataclass_error_to_str(e)}

    results = journal_entries.select_with_filter_paginated(valid_input)

    data_results = results["data"]
    if data_results:
        id_list = [str(journal["id"]) for journal in data_results]

        __validate_journal_entries(id_list)

        lines_list = journal_entries.select_lines_by_journals(id_list)
        att_list = journal_entries.select_attachments_by_journals(id_list)

        for journal_entry in data_results:
            journal_entry_id = journal_entry.pop("id")

            journal_entry["lineItems"] = je_utils.calculate_line_items(lines_list, journal_entry_id)

            journal_entry["attachments"] = je_utils.calculate_attachments(att_list, journal_entry_id)

    journal_entries_ = [JournalEntry(**result) for result in data_results]

    try:
        journal_entries.bulk_state(journal_entry_ids)
    except Exception as e:
        return 500, {"detail": f"An error occurred when updating the state of the journal entries: {str(e)}"}


    chunks = [journal_entry_objects[i:i+40] for i in range(0, len(journal_entry_objects), 40)]

    for chunk in chunks:




    target_queue_url = os.getenv("SQS_QUEUE_URL")



    for chunk in chunks:
        message = {
            'journalEntries': chunk
        }
        try:
            response = sqs.send_message(
                QueueUrl=target_queue_url,
                MessageBody=json.dumps(message, default=str)
            )
            logging.write_log(
                context,
                "Informational",
                "Journal Entry - DB Bulk State",
                f"Sent chunk with {len(chunk)} journal entries, message ID: {response['MessageId']}",
            )
        except Exception as e:
            return 500, {"detail": f"An error occurred when sending journal entry to SQS: {str(e)}"}

    return 200, {}
