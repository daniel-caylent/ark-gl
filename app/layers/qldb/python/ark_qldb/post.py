"""This module helps in posting documents to QLDB layer"""
from hashlib import sha256
import os

from ark_qldb.qldb import Driver

ledger_name = os.getenv("LEDGER_NAME")
aws_region = os.getenv("AWS_REGION")

HASH_NAMES = ["memo", "reference"]
IGNORE_NAMES = ["fs_name", "fs_mapping_id", "fs_mapping_status", "is_taxable", "is_entity_required"]


def post(table_name: str, contents: dict):
    """Submitting a contents dict to QLDB based on table name"""

    if not ledger_name:
        raise Exception("LEDGER_NAME environment variable is missing.")

    driver = Driver(ledger_name, region_name=aws_region)

    contents = process_contents(contents)
    if table_name == "account":
        driver.insert_account(contents)
    elif table_name == "ledger":
        driver.insert_ledger(contents)
    elif table_name == "journal_entry":
        driver.insert_journal_entry(contents)
    else:
        raise Exception(f"Invalid table name: {table_name}")


def post_many(table_name: str, contents: list):
    """Submitting a contents dict to QLDB based on table name"""

    if not ledger_name:
        raise Exception("LEDGER_NAME environment variable is missing.")

    driver = Driver(ledger_name, region_name=aws_region)

    for idx, content in enumerate(contents):
        contents[idx] = process_contents(content)

    if table_name == "account":
        driver.insert_many_accounts(contents)
    elif table_name == "ledger":
        driver.insert_many_ledgers(contents)
    elif table_name == "journal_entry":
        driver.insert_many_journal_entries(contents)
    else:
        raise Exception(f"Invalid table name: {table_name}")


def process_contents(contents):
    """Remove keys that should not be POSTED and apply hashes"""
    processed_contents = {}
    for key, item in contents.items():
        if key in IGNORE_NAMES:
            continue

        if key in HASH_NAMES:
            item = sha256(item.encode("utf-8")).hexdigest()

        if  isinstance(item, list):
            child_list = []
            for child_item in item:
                child_list.append(process_contents(child_item))
            item = child_list

        processed_contents[key] = item
    return processed_contents
