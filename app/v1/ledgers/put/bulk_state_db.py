"""Lambda that will perform PUT requests for Ledgers / state"""
import os
import json
import boto3
from datetime import datetime

# pylint: disable=import-error; Lambda layer dependency
from arkdb import ledgers
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

    ledger_ids = body.get("ledgerIds")
    if not ledger_ids:
        return 400, {"detail": "No ledger ids specified."}

    ledger_objects = []

    for id_ in ledger_ids:
        if not validate_uuid(id_):
            return 400, {"detail": f"Invalid uuid: {id_}"}

        result = ledgers.select_by_id(id_, False)
        if result is None:
            return 404, {"detail": f"No ledger found for: {id_}"}

        if result["state"] == "POSTED":
            return 400, {"detail": f"POSTED ledger cannot be posted: {id_}"}

        ledger_objects.append(result)

    post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        ledgers.bulk_state(ledger_ids, post_date)
    except Exception as e:
        return 500, {"detail": f"An error occurred when updating the state of the ledgers: {str(e)}"}

    for idx in enumerate(ledger_objects):
        ledger_objects[idx]['state'] = 'POSTED'
        ledger_objects[idx]['post_date'] = post_date

    target_queue_url = os.getenv("SQS_QUEUE_URL")

    chunks = [ledger_objects[i:i+40] for i in range(0, len(ledger_objects), 40)]

    for chunk in chunks:
        message = {
            'ledgers': chunk
        }
        try:
            response = sqs.send_message(
                QueueUrl=target_queue_url,
                MessageBody=json.dumps(message, default=str)
            )
            logging.write_log(
                context,
                "Informational",
                "Ledgers - DB Bulk State",
                f"Sent chunk with {len(chunk)} ledgers, message ID: {response['MessageId']}",
            )
        except Exception as e:
            return 500, {"detail": f"An error occurred when sending ledgers to SQS: {str(e)}"}

    return 200, {}
