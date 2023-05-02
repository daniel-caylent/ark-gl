import boto3

from .validate_new_account import validate_new_account

def download_from_s3(signed_s3_url: str) -> str:
    return 'the csv contents'

def convert_csv_to_dicts(csv_str: str) -> list[dict]:
    return [{}]

def import_account_dicts(accounts, fund_id):
    for account in accounts:
        code, detail, post = validate_new_account(account)

def upload(signed_s3_url, fund_id):
    csv_str = download_from_s3(signed_s3_url)
