"""
This Lambda is responsible for splitting up the load from
the JornalEntry QLDB table and distributes the load to be processed
by multiple Lambdas instances
"""
import os
import boto3

from ark_qldb import qldb  # pylint: disable=import-error; Lambda layer dependency


def __divide_chunks(input_list, chunck_size):
    for i in range(0, len(input_list), chunck_size):
        yield input_list[i : i + chunck_size]


def handler(
    event, context # pylint: disable=unused-argument; Required lambda parameters
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
    driver = qldb.Driver("ARKGL", region_name="us-east-1")
    buffered_cursor = driver.read_document_fields("journal_entry", ["uuid"])
    sqs_name = os.getenv("sqs_name")
    processed_list = []

    chunk_size = 4
    sqs = boto3.client("sqs")
    queue = sqs.get_queue_url(QueueName=sqs_name)

    for current_row in buffered_cursor:
        processed_list.append(current_row["uuid"])

    current_chunk = list(__divide_chunks(processed_list, chunk_size))

    for current_chunk_item in current_chunk:
        sqs.send_message(
            QueueUrl=queue["QueueUrl"], MessageBody=str(current_chunk_item)
        )

    return 200, {}
