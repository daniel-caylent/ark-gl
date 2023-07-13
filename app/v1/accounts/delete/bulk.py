"""Lambda that will perform bulk DELETE requests for Accounts"""
import json

# pylint: disable=import-error; Lambda layer dependency
from arkdb import accounts
from shared import endpoint, validate_uuid
# pylint: enable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters
    """Handler for accounts bulk deletes endpoint"""
    if not event.get("queryStringParameters"):
        return 400, {"detail": "Missing query string parameters"}

    try:
        account_ids = json.loads(event["queryStringParameters"].get("accountIds"))
    except BaseException:
        return 400, {"detail": "Unable to parse account IDs."}

    if not account_ids:
        return 400, {"detail": "No accounts specified."}

    for id_ in account_ids:
        if not validate_uuid(id_):
            return 400, {"detail": f"Invalid uuid: {id_}"}

        result = accounts.select_by_id(id_)
        if result is None:
            return 404, {"detail": f"No account found for: {id_}"}

        if result["state"] == "POSTED":
            return 400, {"detail": f"POSTED account cannot be deleted: {id_}"}

    try:
        accounts.bulk_delete(account_ids)
    except Exception as e:
        return 400, {"detail": f"Unable to delete. One of these accounts may have children or journal entries"}

    return 200, {}
