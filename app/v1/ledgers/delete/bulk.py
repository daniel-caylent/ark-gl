"""Lambda that will perform bulk DELETE requests for ledgers"""
import json

# pylint: disable=import-error; Lambda layer dependency
from arkdb import ledgers
from shared import endpoint, validate_uuid
# pylint: enable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters
    """Handler for ledgers bulk deletes endpoint"""
    try:
        body = json.loads(event["body"])
    except Exception:
        return 400, {"detail": "Body does not contain valid json."}

    try:
        ledger_ids = body.get("ledgerIds")
    except BaseException:
        return 400, {"detail": "Unable to parse ledger IDs."}

    if not ledger_ids:
        return 400, {"detail": "No ledgers specified."}

    for id_ in ledger_ids:
        if not validate_uuid(id_):
            return 400, {"detail": f"Invalid uuid: {id_}"}

        result = ledgers.select_by_id(id_)
        if result is None:
            return 404, {"detail": f"No ledger found for: {id_}"}

        if result["state"] == "POSTED":
            return 400, {"detail": f"POSTED ledger cannot be deleted: {id_}"}

    try:
        ledgers.bulk_delete(ledger_ids)
    except Exception as e:
        return 400, {"detail": f"{str(e)}. Ledger may have journal entries."}

    return 200, {}
