"""Lambda that will perform Ledgers PUT"""

import json

# pylint: disable=import-error; Lambda layer dependency
from arkdb import ledgers
from shared import endpoint, validate_uuid, update_dict, dataclass_error_to_str
from models import LedgerPut
# pylint: enable=import-error

COMMITED_CHANGEABLE = []
REQUIRED_FIELDS = ["fundId", "glName", "currencyName", "currencyDecimal"]


@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters
    """Handler for ledgers PUT request

    event: dict
    POST event passed in from API gateway. The key 'body' should
    cary the POST request as a JSON string

    context: LambdaContext
    Context about the instance of the lambda function
    """
    if not event.get("pathParameters"):
        return 400, {"detail": "Missing path parameters"}

    ledger_id = event["pathParameters"].get("ledgerId", None)
    if ledger_id is None:
        return 400, {"detail": "No ledger specified."}

    if not validate_uuid(ledger_id):
        return 400, {"detail": "Invalid ledger UUID."}

    # validate the request body
    try:
        body = json.loads(event["body"])
    except Exception():
        return 400, {"detail": "Body does not contain valid json."}

    if len(body.keys()) == 0:
        return 400, {"detail": "Body does not contain content."}

    # validate the PUT contents
    try:
        put = LedgerPut(**body)
    except Exception as e:
        return 400, {"detail": dataclass_error_to_str(e)}

    # verify ledger exists
    ledger = ledgers.select_by_id(ledger_id)
    if ledger is None:
        return 404, {"detail": "No ledger found."}

    if ledger['state'] == 'POSTED':
        for key in body.keys():
            if key not in COMMITED_CHANGEABLE:
                return 400, {'detail': f"POSTED ledger property cannot be modified: {key}."}

    # validate no other ledgers exist with the same name
    ledgers_ = ledgers.select_by_fund_id(ledger["fundId"])
    unique = validate_unique_ledger(ledger_id, put, ledgers_)
    if unique is False:
        return 409, {"detail": "Ledger name already exists in this fund."}

    # only keep fields present in the initial body, but replace
    # with type safe values from dataclass
    type_safe_body = update_dict(body, put.__dict__)

    missing = check_missing_fields(type_safe_body, REQUIRED_FIELDS)
    if missing is not None:
        return 400, {"detail": f"{missing} cannot be null or empty."}

    ledgers.update_by_id(ledger_id, type_safe_body)
    return 200, {}


def validate_unique_ledger(ledger_id: str, ledger: LedgerPut, existing_ledgers):
    """Validate the incoming ledger has a unique name"""

    for ledger_ in existing_ledgers:
        if ledger_["ledgerId"] == ledger_id:
            continue

        if ledger.glName:
            if ledger_["glName"].lower() == ledger.glName.lower():
                return False
    return True


def check_missing_fields(dict_, required):
    """
    Check that the ledger information about to be updated does not input
    any null values for required fields
    """
    keys = list(dict_.keys())
    for field in required:
        if field in keys:
            value = dict_[field]

            if value is None or value == "":
                return field

    return None
