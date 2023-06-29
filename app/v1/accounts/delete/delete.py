"""Lambda that will perform DELETE requests for Accounts"""

# pylint: disable=import-error; Lambda layer dependency
from arkdb import accounts
from shared import endpoint, validate_uuid
# pylint: enable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters
    if not event.get("pathParameters"):
        return 400, {"detail": "Missing path parameters"}

    account_id = event["pathParameters"].get("accountId", None)
    if account_id is None:
        return 400, {"detail": "No account specified."}

    if not validate_uuid(account_id):
        return 400, {"detail": "Invalid UUID provided."}

    result = accounts.select_by_id(account_id)
    if result is None:
        return 404, {"detail": "No account found."}

    if result["state"] == "POSTED":
        return 400, {"detail": "POSTED accounts cannot be deleted."}

    try:
        accounts.delete_by_id(account_id)
    except Exception as e:
        return 400, {"detail": f"Unable to delete. This account may have children or journal entries."}

    return 200, {}
