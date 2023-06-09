"""Lambda responsible for creating the QLDB tables in AWS"""

import os
from logging import getLogger

from ark_qldb import qldb # pylint: disable=import-error; Lambda layer dependency

logger = getLogger(__name__)


def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters
    """Main handler method for the Lambda function
    that will create tables in the QLDB ledger with their indexes"""
    ledger_name = os.getenv("LEDGER_NAME")
    region_name = os.getenv("AWS_REGION")
    driver = qldb.Driver(ledger_name, region_name=region_name)

    tables_to_create = ["account", "ledger", "journal_entry"]

    for table in tables_to_create:
        logger.info("Checking if table %s exists", table)
        checking_query = (
            "SELECT name FROM information_schema.user_tables WHERE name = '"
            + table
            + "' AND status = 'ACTIVE';"
        )
        result_cursor = driver.execute_custom_query(checking_query)
        if not next(result_cursor, None):
            # If it does not exist, create the table and its indexes
            logger.info("Creating table %s", table)
            driver.create_table(table)
            driver.create_index(table, ["id"])
            driver.create_index(table, ["uuid"])
            driver.create_index(table, ["created_on"])
            driver.create_index(table, ["fund_entity_id"])

    return 200, {}
