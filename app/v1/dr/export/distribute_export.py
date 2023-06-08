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
    # Configure the S3 and SQS clients
    s3_client = boto3.client("s3")
    sqs_client = boto3.client("sqs")

    # Retrieve the name of the source S3 bucket and target SQS queue from the event
    source_bucket = os.getenv("DR_BUCKET_NAME")
    target_queue_url = os.getenv("SQS_QUEUE_URL")

    # List all objects in the source bucket
    try:
        response = s3_client.list_objects_v2(Bucket=source_bucket)
    except Exception as e:
        logging.write_log(
            event,
            context,
            "Error",
            "DR Export Error when listing objects in bucket: " + source_bucket,
            str(e),
        )
        raise

    # Check if any objects are present in the bucket
    if "Contents" in response:
        # Extract the object keys
        object_keys = [obj["Key"] for obj in response["Contents"]]

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
                        event,
                        context,
                        "Error",
                        "DR Export Error when publishing message to SQS queue",
                        str(e),
                    )
                    raise

    return 200, {}
