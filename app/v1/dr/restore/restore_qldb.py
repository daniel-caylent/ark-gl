import os
import awswrangler as wr
import json
from shared import logging
from ark_qldb import qldb

region = os.getenv("AWS_REGION")
dr_bucket_name = os.getenv("dr_bucket_name")
ledger_name = os.getenv("LEDGER_NAME")

def handler(event, context) -> tuple[int, dict]:

    dr_bucket_prefix = event.get("file")
    
    s3_path = 's3://'+dr_bucket_name+'/'+dr_bucket_prefix.lstrip('/')

    df = wr.s3.read_json(path=s3_path, lines=True)
    df_to_json_array = json.loads(df.to_json(orient='records'))

    docs_to_insert = []
    for item in df_to_json_array:
        for statement in item['transactionInfo']['statements']:
            if statement['statement'].upper().startswith("INSERT INTO"):
                docs_to_insert.append(
                    {
                        'statement': statement['statement'],
                        'data': item['revisions'][0]['data']
                    }
                )
    
    driver = qldb.Driver(ledger_name, region_name=region)

    try:
        for doc in docs_to_insert:
            driver.execute_custom_query_with_params(
                doc['statement'],
                doc['data']
            )
    except Exception as e:
        logging.write_log(
            event, context, "Error", "DR Restore Error in file:" + s3_path, str(e), 
        )
        raise
    
    logging.write_log(
        event, context, "Notice", "DR Restore Info", "Restored file:" + s3_path
    )
    return 200, {}
