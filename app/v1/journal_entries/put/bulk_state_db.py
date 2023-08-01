"""Lambda that will perform PUT requests for Journal Entries / state"""
import os
import json
import boto3
from datetime import datetime

# pylint: disable=import-error; Lambda layer dependency
from arkdb import journal_entries
from shared import (
    endpoint,
    validate_uuid,
    logging,
    filtering,
    dataclass_error_to_str,
    s3_utils
)
from journal_entries_shared import utils as je_utils
#from models import JournalEntry
# pylint: enable=import-error

sqs = boto3.client('sqs')
s3 = boto3.client('s3')


JE_BULK_STATE_BUCKET = os.getenv("JOURNAL_ENTRIES_BULK_STATE_BUCKET_NAME")


def __validate_journal_entries(journal_entry_uuids: []):
    for uuid_ in journal_entry_uuids:
        if not validate_uuid(uuid_):
            return 400, {"detail": f"Invalid uuid: {uuid_}"}

        result = journal_entries.select_by_id(uuid_, False)
        if result is None:
            return 404, {"detail": f"No journal entry found for: {uuid_}"}

        if result["state"] == "POSTED":
            return 400, {"detail": f"POSTED journal entry cannot be posted: {uuid_}"}

    records = journal_entries.select_draft_accounts_and_ledgers_by_id_list_query(journal_entry_uuids)

    if records:
        return 400, {"detail": f"The following Accounts and/or Ledgers are not in the POSTED state: {json.dumps(records, indent=2)}"}

    return None

@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters

    try:
        body = json.loads(event["body"])
    except Exception:
        return 400, {"detail": "Body does not contain valid json."}

    try:
        valid_input = filtering.FilterInput(**body).get_dict()
    except Exception as e:
        return 400, {"detail": dataclass_error_to_str(e)}

    results = journal_entries.select_with_filter_paginated(valid_input, translate=False)

    data_results = results["data"]
    if data_results:

        uuid_list = [str(journal["uuid"]) for journal in data_results]
        error = __validate_journal_entries(uuid_list)

        if error:
            return error

        id_list = [str(journal["id"]) for journal in data_results]

        lines_list = journal_entries.select_lines_by_journals(id_list)
        att_list = journal_entries.select_attachments_by_journals(id_list)

        for journal_entry in data_results:
            journal_entry_id = journal_entry.pop("id")
            journal_entry["lineItems"] = je_utils.calculate_line_items(lines_list, journal_entry_id)
            journal_entry["attachments"] = je_utils.calculate_attachments(att_list, journal_entry_id)

        post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            journal_entries.bulk_state(uuid_list, post_date)
        except Exception as e:
            return 500, {"detail": f"An error occurred when updating the state of the journal entries: {str(e)}"}

        for idx in enumerate(data_results):
            data_results[idx]['state'] = 'POSTED'
            data_results[idx]['post_date'] = post_date

        chunks = [data_results[i:i+40] for i in range(0, len(data_results), 40)]

        s3_filenames = []

        for idx, chunk in enumerate(chunks):
            s3_filename = s3_utils.save_to_s3(s3, chunk, JE_BULK_STATE_BUCKET, context.aws_request_id, str(idx))
            s3_filenames.append(s3_filename)

        target_queue_url = os.getenv("SQS_QUEUE_URL")

        for s3_filename in s3_filenames:
            message = {
                'journalEntriesS3Path': s3_filename,
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
                    f"Sent chunk {s3_filename} with journal entries, message ID: {response['MessageId']}",
                )
            except Exception as e:
                return 500, {"detail": f"An error occurred when sending journal entry to SQS: {str(e)}"}

    return 200, {}
