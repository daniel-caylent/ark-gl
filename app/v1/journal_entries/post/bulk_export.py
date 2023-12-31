"""Lambda that will perform the GET for JournalEntries"""

import uuid
import os
import json
import boto3

# pylint: disable=import-error; Lambda layer dependency
from arkdb import journal_entries
from journal_entries_shared import utils as je_utils
from shared import endpoint, dataclass_error_to_str, filtering
# pylint: enable=import-error


EXTRA_FILTERS_ALLOWED = ['startDate', 'endDate', 'journalEntryState']


@endpoint
def handler(event, context) -> tuple[int, dict]:  # pylint: disable=unused-argument; Required lambda parameters
    """Get journal entries by ledgerId"""

    try:
        body = json.loads(event["body"])
    except Exception:
        return 400, {"detail": "Body does not contain valid json."}

    try:
        body['parse'] = False
        valid_input = filtering.FilterInput(**body).get_dict()
    except Exception as e:
        return 400, {"detail": dataclass_error_to_str(e)}

    results = journal_entries.select_with_filter_paginated(valid_input)

    data_results = results["data"]

    if data_results:
        id_list = [str(journal["id"]) for journal in data_results]
        lines_list = journal_entries.select_lines_by_journals(id_list)
        att_list = journal_entries.select_attachments_by_journals(id_list)

        for journal_entry in data_results:
            journal_entry_id = journal_entry.pop("id")

            journal_entry["lineItems"] = je_utils.calculate_line_items(lines_list, journal_entry_id)

            journal_entry["attachments"] = je_utils.calculate_attachments(att_list, journal_entry_id)

    s3_bucket = os.getenv("EXPORT_BUCKET_NAME")
    s3_key = f'journal_entries/{str(uuid.uuid4())}.txt'

    s3_client = boto3.client('s3')
    s3_client.put_object(
        Body=json.dumps(data_results, default=str),
        Bucket=s3_bucket,
        Key=s3_key,
    )

    s3_signed_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': s3_bucket, 'Key': s3_key},
    )

    return 201, {"s3SignedUrl": s3_signed_url}
