"""
This Lambda is responsible for exporting the Ledger from the ARK QLDB database to S3
"""
import os
from datetime import datetime, timedelta
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
    dr_bucket_name = os.getenv("DR_BUCKET_NAME")
    ledger_name = os.getenv("LEDGER_NAME")
    region = os.getenv("AWS_REGION")
    role_arn = os.getenv("ROLE_ARN")
    qldb_export_trigger_hour = os.getenv("QLDB_EXPORT_TRIGGER_HOUR")

    # Configure the AWS SDK with your credentials and desired region
    session = boto3.Session(region_name=region)
    qldb_client = session.client("qldb")

    time_end = datetime.now().replace(minute=0, second=0, microsecond=0)
    time_start = time_end - timedelta(hours=int(qldb_export_trigger_hour))
    # Specify the QLDB ledger name and export configuration
    export_config = {
        "Bucket": dr_bucket_name,
        "Prefix": "arkgl-dr/",
        "EncryptionConfiguration": {"ObjectEncryptionType": "SSE_S3"},
    }

    # Trigger the export by calling the ExportJournalToS3 API
    response = qldb_client.export_journal_to_s3(
        Name=ledger_name,
        S3ExportConfiguration=export_config,
        InclusiveStartTime=time_start,
        ExclusiveEndTime=time_end,
        RoleArn=role_arn,
        OutputFormat="JSON",
    )

    # Print the export job ID
    export_job_id = response["ExportId"]
    logging.write_log(
        event, context, "Notice", "DR Export Info", "Export Job ID:" + export_job_id
    )

    return 200, {}
