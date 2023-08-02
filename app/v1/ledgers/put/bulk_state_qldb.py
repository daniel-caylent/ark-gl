"""Lambda that will perform inserts for Ledgers into QLDB"""
import json

# pylint: disable=import-error; Lambda layer dependency
from ark_qldb.post import post_many
from shared import endpoint, dataclass_encoder, logging
# pylint: enable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters
    """Ledger bulk State, QLDB"""
    try:
        # This lambda is configured to receive only a single record at time,
        # so it is safe to access [0]
        body = json.loads(event['Records'][0]['body'])
    except Exception as e:
        raise RuntimeError("The event does not contain valid json.") from e

    encoded_ledgers = []
    for account in body['ledgers']:
        encoded_ledgers.append(dataclass_encoder.encode(account))

    post_many("ledger", encoded_ledgers)

    message_id = event['Records'][0]['messageId']

    logging.write_log(
        context,
        "Informational",
        "Ledgers - QLDB Bulk State",
        f'Inserted {len(body["ledgers"])} ledgers in QLDB from message id {message_id}',
    )

    return 200, {}
