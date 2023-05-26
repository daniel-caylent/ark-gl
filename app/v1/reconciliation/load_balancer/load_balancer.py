import boto3
from ark_qldb import qldb
import os


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i : i + n]


def handler(event, context) -> tuple[int, dict]:
    driver = qldb.Driver("ARKGL", region_name="us-east-1")
    buffered_cursor = driver.read_document_fields(
        "journal_entry", ["uuid"]
    )
    sqs_name = os.getenv("sqs_name")
    processed_list = []
    i = 0
    CHUNK_SIZE = 4
    sqs = boto3.client("sqs")
    queue = sqs.get_queue_url(QueueName=sqs_name)

    for current_row in buffered_cursor:
        processed_list.append(
            current_row["uuid"]
        )

    x = list(divide_chunks(processed_list, CHUNK_SIZE))

    for current_chunk in x:
        sqs.send_message(QueueUrl=queue["QueueUrl"], MessageBody=str(current_chunk))
        # client is required to interact with

    return 200, {}
