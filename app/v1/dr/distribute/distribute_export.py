"""
This Lambda is responsible for splitting up the load from
the QLDB exports distributes the load to be processed
by multiple Lambdas instances
"""
import os
import boto3

# pylint: disable=import-error; Lambda layer dependency
from shared import (
    endpoint,
    logging,
)

# pylint: enable=import-error


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
    try:
        object_keys = []
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=source_bucket)

        for page in pages:
            for obj in page["Contents"]:
                object_keys.append(obj["Key"])
    except Exception as e:
        logging.write_log(
            context,
            "Error",
            "DR Export Error when listing objects in bucket: " + source_bucket,
            str(e),
        )
        raise

    # Push each object key to the SQS queue
    for object_key in object_keys:
        if object_key.endswith(".json"):
            try:
                sqs_client.send_message(
                    QueueUrl=target_queue_url,
                    MessageBody="s3://" + source_bucket + "/" + object_key,
                )
            except Exception as e:
                logging.write_log(
                    context,
                    "Error",
                    "DR Export Error when publishing message to SQS queue",
                    str(e),
                )
                raise

    return 200, {}
