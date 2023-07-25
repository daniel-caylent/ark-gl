"""Lambda that will perform PUT requests for Accounts"""

import json

# pylint: disable=import-error; Lambda layer dependency
from arkdb import accounts, account_attributes
from shared import endpoint, validate_uuid, update_dict, dataclass_error_to_str
from models import AccountPut
from shared_validators import (
    validate_fs_account,
    validate_parent_account,
    validate_unique_account,
    check_missing_fields,
)

# pylint: enable=import-error

COMMITED_CHANGEABLE = ["fsName", "fsMappingId"]


@endpoint
def handler(
    event, context
) -> tuple[int, dict]:  # pylint: disable=unused-argument; Required lambda parameters
    if not event.get("pathParameters"):
        return 400, {"detail": "Missing path parameters"}

    account_id = event["pathParameters"].get("accountId", None)
    if account_id is None:
        return 400, {"detail": "No account specified."}

    if not validate_uuid(account_id):
        return 400, {"detail": "Invalid account UUID."}

    # validate the request body
    try:
        body = json.loads(event["body"])
    except Exception:
        return 400, {"detail": "Body does not contain valid json."}

    if len(body.keys()) == 0:
        return 400, {"detail": "Body does not contain content."}

    # validate the PUT contents
    try:
        put = AccountPut(**body)

        if "fsMappingId" in body:
            body["fsMappingStatus"] = None
            put.update_fs()

    except Exception as e:
        return 400, {"detail": dataclass_error_to_str(e)}

    # verify account exists
    acct = accounts.select_by_id(account_id)
    if acct is None:
        return 404, {"detail": "No account found."}

    if acct["state"] == "POSTED":
        for key in body.keys():
            if key not in COMMITED_CHANGEABLE:
                return 400, {
                    "detail": f"POSTED account property cannot be modified: {key}."
                }

    # validate no other accounts exist with number or name
    accts = accounts.select_by_fund_id(acct["fundId"])
    unique = validate_unique_account(account_id, put, accts)
    if unique is False:
        return 409, {"detail": "Account number or name already exists in this fund."}

    # validate parent exists if part of this request
    if put.parentAccountId:
        parent = validate_parent_account(put, accts)
        if not parent:
            return 400, {"detail": "Parent account does not exist in this fund."}

    if put.fsMappingId:
        if not validate_fs_account(put, accts):
            return 400, {
                "detail": "fsMappingId does not relate to an existing account."
            }

    # if an attribute is part of this request, validate it exists
    if put.attributeId:
        attribute = account_attributes.select_by_id(put.attributeId)
        if not attribute:
            return 400, {"detail": "Account attribute does not exist."}

    # only keep fields present in the initial body, but replace
    # with type safe values from dataclass
    type_safe_body = update_dict(body, put.__dict__)

    missing = check_missing_fields(type_safe_body)
    if missing is not None:
        return 400, {"detail": f"{missing} cannot be null or empty."}

    accounts.update_by_id(account_id, type_safe_body)
    return 200, {}
