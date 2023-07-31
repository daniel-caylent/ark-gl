"""Lambda that will perform PUT requests for Journal Entries / state"""
import os
import json
import boto3

# pylint: disable=import-error; Lambda layer dependency
from arkdb import journal_entries
from shared import endpoint, validate_uuid, logging
# pylint: enable=import-error

sqs = boto3.client('sqs')

@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters

    # validate the request body
    try:
        body = json.loads(event["body"])
    except Exception:
        return 400, {"detail": "Body does not contain valid json."}

    journal_entry_ids = body.get("journalEntryIds")
    if not journal_entry_ids:
        return 400, {"detail": "No journal entry ids specified."}

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

    try:
        journal_entries.bulk_state(journal_entry_ids)
    except Exception as e:
        return 500, {"detail": f"An error occurred when updating the state of the journal entries: {str(e)}"}


    target_queue_url = os.getenv("SQS_QUEUE_URL")

    chunks = [journal_entry_objects[i:i+40] for i in range(0, len(journal_entry_objects), 40)]

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
