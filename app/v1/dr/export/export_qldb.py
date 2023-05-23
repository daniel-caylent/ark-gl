import json
from ark_qldb import qldb
from random import random
from arkdb import accounts
from shared import endpoint, logging
import boto3
import os

@endpoint
def handler(event, context) -> tuple[int, dict]:
    dr_bucket_name = os.getenv("dr_bucket_name")
    ledger_name = os.getenv("ledger_name")
    region = os.getenv("region")
    # Configure the AWS SDK with your credentials and desired region
    session = boto3.Session(region_name=region)
    qldb_client = session.client('qldb')

    # Specify the QLDB ledger name and export configuration
    export_config = {
        'S3Bucket': dr_bucket_name,
        #'RoleArn': 'arn:aws:iam::your-account-id:role/your-role-name'
    }

    # Trigger the export by calling the ExportJournalToS3 API
    response = qldb_client.export_journal_to_s3(Name=ledger_name, S3ExportConfiguration=export_config)

    # Print the export job ID
    export_job_id = response['ExportId']
    logging.write_log(
                event, context, "Notice", "DR Export Infor", "Export Job ID:" + export_job_id
            )  # record exists in QLDB and not in Aurora. Someone deleted it)
    return 200, {}