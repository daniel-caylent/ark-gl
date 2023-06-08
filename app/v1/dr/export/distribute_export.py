# TODO: consider adding a meaningful description to this module
"""
This Lambda is responsible for
"""
import os

import boto3
from shared import endpoint # pylint: disable=import-error; Lambda layer dependency


@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters
    """
    Lambda entry point

    event: object
    Event passed when the lambda is triggered

    context: object
    Lambda Context

    return: tuple[int, dict]
    Success code and an empty object
    """
    # Configure the S3 and SQS clients
    s3_client = boto3.client("s3")
    sqs_client = boto3.client("sqs")

    # Retrieve the name of the source S3 bucket and target SQS queue from the event
    source_bucket = os.getenv("DR_BUCKET_NAME")
    target_queue_url = os.getenv("SQS_QUEUE_URL")

    # List all objects in the source bucket
    response = s3_client.list_objects_v2(Bucket=source_bucket)

    # Check if any objects are present in the bucket
    if "Contents" in response:
        # Extract the object keys
        object_keys = [obj["Key"] for obj in response["Contents"]]

        # Push each object key to the SQS queue
        for object_key in object_keys:
            if object_key.endswith(".json"):
                sqs_client.send_message(
                    QueueUrl=target_queue_url,
                    MessageBody="s3://" + source_bucket + "/" + object_key,
                )
    # TODO: this lambda is not logging its processing, consider adding some

    return (200, {})
