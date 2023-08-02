"""Lambda that will perform PUT requests for Accounts / state"""
import os
import json
from datetime import datetime

import boto3

# pylint: disable=import-error; Lambda layer dependency
from arkdb import accounts
from shared import endpoint, validate_uuid, logging
# pylint: enable=import-error

sqs = boto3.client('sqs')

@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters
    """Bulk state aurora"""
    # validate the request body
    try:
        body = json.loads(event["body"])
    except Exception:
        return 400, {"detail": "Body does not contain valid json."}

    account_ids = body.get("accountIds")
    if not account_ids:
        return 400, {"detail": "No account ids specified."}

    account_objects = []

    for id_ in account_ids:
        if not validate_uuid(id_):
            return 400, {"detail": f"Invalid uuid: {id_}"}

        result = accounts.select_by_id(id_, False)
        if result is None:
            return 404, {"detail": f"No account found for: {id_}"}

        if result["state"] == "POSTED":
            return 400, {"detail": f"POSTED account cannot be posted: {id_}"}

        account_objects.append(result)

    post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        accounts.bulk_state(account_ids, post_date)
    except Exception as e:
        return 500, {"detail": f"An error occurred when updating the state of the accounts: {str(e)}"}

    for data in account_objects:
        data['state'] = 'POSTED'
        data['post_date'] = post_date

    target_queue_url = os.getenv("SQS_QUEUE_URL")

    chunks = [account_objects[i:i+40] for i in range(0, len(account_objects), 40)]

    for chunk in chunks:
        message = {
            'accounts': chunk
        }
        try:
            response = sqs.send_message(
                QueueUrl=target_queue_url,
                MessageBody=json.dumps(message, default=str)
            )
            logging.write_log(
                context,
                "Informational",
                "Accounts - DB Bulk State",
                f"Sent chunk with {len(chunk)} accounts, message ID: {response['MessageId']}",
            )
        except Exception as e:
            return 500, {"detail": f"An error occurred when sending accounts to SQS: {str(e)}"}

    return 200, {}
