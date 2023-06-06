import os

from .qldb import Driver

ledger_name = os.getenv("LEDGER_NAME")
aws_region = os.getenv("AWS_REGION")

def post(table_name: str, contents: dict):
    if not ledger_name:
        raise Exception("LEDGER_NAME environment variable is missing.")

    driver = Driver(ledger_name, region_name=aws_region)

    if table_name == "account":
        driver.insert_account(contents)
    elif table_name == "ledger":
        driver.insert_ledger(contents)
    elif table_name == "journal-entry":
        driver.insert_journal_entry(contents)
    else:
        raise Exception("Invalid table name.")
