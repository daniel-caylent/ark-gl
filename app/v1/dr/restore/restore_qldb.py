# TODO - consider a meaningful description for this file
"""
This Lambda is responsible for
"""
import os
import json

# pylint: disable=import-error; Lambda layer dependency
import awswrangler as wr
from shared import logging
from ark_qldb import qldb
# pylint: enable=import-error

region = os.getenv("AWS_REGION")
ledger_name = os.getenv("LEDGER_NAME")

# TODO - missing endpoint decorator
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
    # Reading from SQS queue
    for record in event["Records"]:
        s3_path = record["body"]

        # TODO: consider renaming `df` to a more meaningful name
        df = wr.s3.read_json(path=s3_path, lines=True)
        df_to_json_array = json.loads(df.to_json(orient="records"))

        docs_to_insert = []
        for item in df_to_json_array:
            for statement in item["transactionInfo"]["statements"]:
                if statement["statement"].upper().startswith("INSERT INTO"):
                    docs_to_insert.append(
                        {
                            "statement": statement["statement"],
                            "data": item["revisions"][0]["data"],
                        }
                    )

        driver = qldb.Driver(ledger_name, region_name=region)

        try:
            for doc in docs_to_insert:
                driver.execute_custom_query(doc["statement"], doc["data"])
        except Exception as e:
            logging.write_log(
                event,
                context,
                "Error",
                "DR Restore Error in file:" + s3_path,
                str(e),
            )
            raise

        logging.write_log(
            event, context, "Notice", "DR Restore Info", "Restored file:" + s3_path
        )

    return 200, {}
