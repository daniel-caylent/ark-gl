"""Lambda that will perform inserts for Journal Entries into QLDB"""
import os
import json

import boto3


# pylint: disable=import-error; Lambda layer dependency
import ark_qldb
from shared import endpoint, dataclass_encoder, logging, s3_utils
# pylint: enable=import-error

s3 = boto3.client('s3')

JE_BULK_STATE_BUCKET = os.getenv("JOURNAL_ENTRIES_BULK_STATE_BUCKET_NAME")

@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters

    try:
        # This lambda is configured to receive only a single record at time,
        # so it is safe to access [0]
        body = json.loads(event['Records'][0]['body'])
    except Exception as e:
        raise RuntimeError("The event does not contain valid json.") from e

    s3_file_path = body['journalEntriesS3Path']

    records = s3_utils.load_from_s3(s3, s3_file_path)
    try:
        encoded_journal_entries = []
        for journal_entry in records:
            encoded_journal_entries.append(dataclass_encoder.encode(journal_entry))

        ark_qldb.post_many("journal_entry", encoded_journal_entries)

        message_id = event['Records'][0]['messageId']

        logging.write_log(
            context,
            "Informational",
            "Journal Entries - QLDB Bulk State",
            f'Inserted {len(records)} journal entries in QLDB from message id {message_id}',
        )
    finally:
        s3_utils.delete_from_s3(s3, s3_file_path)

    return 200, {}
