"""
This Lambda is responsible for splitting up the load from
the JornalEntry QLDB table and distributes the load to be processed
by multiple Lambdas instances
"""
import os
import json
import uuid

import boto3

from ark_qldb import qldb  # pylint: disable=import-error; Lambda layer dependency

region_name = os.getenv("AWS_REGION")


def __divide_chunks(input_list, chunck_size):
    for i in range(0, len(input_list), chunck_size):
        yield input_list[i : i + chunck_size]

def handler(
    event, context  # pylint: disable=unused-argument; Required lambda parameters
) -> tuple[int, dict]:
    """
    Lambda entry point

    event: object
    Event passed when the lambda is triggered

    context: object
    Lambda Context

    return: tuple[int, dict]
    Success code and an empty object
    """
    driver = qldb.Driver("ARKGL", region_name=region_name)
    buffered_cursor = driver.read_document_fields("journal_entry", ["uuid"])
    sqs_name = os.getenv("sqs_name")
    processed_list = []

    chunk_size = 1000
    # sqs = boto3.client("sqs")
    # queue = sqs.get_queue_url(QueueName=sqs_name)

    for current_row in buffered_cursor:
        processed_list.append(current_row["uuid"])

    chunks = list(__divide_chunks(processed_list, chunk_size))

    # for current_chunk_item in current_chunk:
    #     sqs.send_message(
    #         QueueUrl=queue["QueueUrl"], MessageBody=str(current_chunk_item)
    #     )

    urls = []
    for chunk in chunks:
        s3_bucket = os.getenv("BUCKET_NAME")
        s3_key = f'journal_entries/reconciliation/{str(uuid.uuid4())}.txt'

        s3_client = boto3.client('s3')
        s3_client.put_object(
            Body=json.dumps(chunk, default=str),
            Bucket=s3_bucket,
            Key=s3_key,
        )

        urls.append({
            "url": s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': s3_bucket, 'Key': s3_key},
        )})

    return urls
