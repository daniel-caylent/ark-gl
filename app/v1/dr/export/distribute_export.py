import json
from random import random
from shared import endpoint, logging
import boto3
import os
from datetime import datetime, timedelta

@endpoint
def handler(event, context) -> tuple[int, dict]:
    # Configure the S3 and SQS clients
    s3 = boto3.client('s3')
    sqs = boto3.client('sqs')

    # Retrieve the name of the source S3 bucket and target SQS queue from the event
    source_bucket = os.getenv("DR_BUCKET_NAME")
    target_queue_url = os.getenv("SQS_QUEUE_URL")

    # List all objects in the source bucket
    response = s3.list_objects_v2(Bucket=source_bucket)

    # Check if any objects are present in the bucket
    if 'Contents' in response:
        # Extract the object keys
        object_keys = [obj['Key'] for obj in response['Contents']]

        # Push each object key to the SQS queue
        for object_key in object_keys:
            if object_key.endswith('.json'):
                sqs.send_message(
                 QueueUrl=target_queue_url,
                 MessageBody="s3://"+source_bucket+"/"+object_key
             )

    return (200,{})


