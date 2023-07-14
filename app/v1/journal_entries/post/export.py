"""Lambda that will perform the GET for JournalEntries"""

import uuid
import os
import json
import boto3

# pylint: disable=import-error; Lambda layer dependency
from arkdb import journal_entries
from shared import (
    endpoint,
    validate_uuid,
)
# pylint: enable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]:  # pylint: disable=unused-argument; Required lambda parameters
    """Get journal entries by ledgerId"""

    try:
        body = json.loads(event["body"])
    except Exception:
        return 400, {"detail": "Body does not contain valid json."}

    has_ledger_ids = body.get("ledgerIds", None) is not None
    has_fund_ids = body.get("fundIds", None) is not None

    if has_ledger_ids and has_fund_ids:
        return 400, {"detail": "The API accepts Ledger IDs OR Fund IDs, but not both in the same request."}

    if has_ledger_ids:
        _ids = body.get("ledgerIds")
    elif has_fund_ids:
        _ids = body.get("fundIds")
    else:
        return 400, {"detail": "Ledger IDs or Fund IDs should be provided."}

    if has_ledger_ids:
        query_filter = {
            "ledgerIds": _ids
        }
    elif has_fund_ids:
        query_filter = {
            "fundIds": _ids
        }

    for id_ in _ids:
        if not validate_uuid(id_):
            return 400, {"detail": "Invalid UUID provided."}

    results = journal_entries.select_with_filter_paginated(query_filter)

    data_results = results["data"]

    if data_results:
        id_list = [str(journal["id"]) for journal in data_results]
        lines_list = journal_entries.select_lines_by_journals(id_list)
        att_list = journal_entries.select_attachments_by_journals(id_list)

        for journal_entry in data_results:
            journal_entry_id = journal_entry.pop("id")

            journal_entry["lineItems"] = __calculate_line_items(lines_list, journal_entry_id)

            journal_entry["attachments"] = __calculate_attachments(att_list, journal_entry_id)

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

    return 201, {"s3_signed_url": s3_signed_url}


def __calculate_attachments(att_list, journal_entry_id):
    return [
        {
            key: value
            for key, value in entry.items()
            if key != "journal_entry_id"
        }
        for entry in list(
            filter(
                lambda att: att["journal_entry_id"] == journal_entry_id,
                att_list,
            )
        )
    ]


def __calculate_line_items(lines_list, journal_entry_id):
    return [
        {
            key: value
            for key, value in entry.items()
            if key != "journal_entry_id"
        }
        for entry in list(
            filter(
                lambda line: line["journal_entry_id"] == journal_entry_id,
                lines_list,
            )
        )
    ]
