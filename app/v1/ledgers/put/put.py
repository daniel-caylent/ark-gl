import json

from arkdb import ledgers
from shared import (
    endpoint,
    validate_uuid,
    update_dict
  )
from models import LedgerPut

COMMITED_CHANGEABLE = []
REQUIRED_FIELDS = [    
    'fundId', 'glName', 'currencyName', 'currencyDecimals'
]

@endpoint
def handler(event, context) -> tuple[int, dict]:
    if not event.get('pathParameters'):
        return 400, {'detail': "Missing path parameters"}

    ledger_id = event['pathParameters'].get('ledgerId', None)
    if ledger_id is None:
        return 400, {'detail': "No ledger specified."}

    if not validate_uuid(ledger_id):
        return 400, {'detail': "Invalid ledger UUID."}

    # validate the request body
    try:
        body = json.loads(event['body'])
    except:
        return 400, {'detail': "Body does not contain valid json."}

    if len(body.keys()) == 0:
        return 400, {'detail': "Body does not contain content."}

    # validate the PUT contents
    try:
        put = LedgerPut(**body)
    except Exception as e:
        remove_str = "__init__() got an "
        remove_str = "__init__() "
        error_str = str(e).strip(remove_str)

        return 400, {'detail': error_str[0].upper() + error_str[1:]}

    # verify account exists
    ledger = ledgers.select_by_id(ledger_id)
    if ledger is None:
        return 404, {'detail': "No ledger found."}

    if ledger['state'] == 'POSTED':
        for key in body.keys():
            if key not in COMMITED_CHANGEABLE:
                return 400, {'detail': f"Ledger property cannot be modified: {key}"}

    # validate no other accounts exist with number or name
    ledgers_ = ledgers.select_by_fund_id(put.fundId)
    unique = validate_unique_ledger(ledger_id, put, ledgers_)
    if unique is False:
        return 409, {'detail': "Account number or name already exists in this fund."}
    

    # only keep fields present in the initial body, but replace
    # with type safe values from dataclass
    type_safe_body = update_dict(body, put.__dict__)

    missing = check_missing_fields(type_safe_body, REQUIRED_FIELDS)
    if missing is not None:
        return 400, {'detail': f"{missing} cannot be null or empty."}

    ledgers.update_by_id(ledger_id, type_safe_body)
    return 200, {}


def validate_unique_ledger(ledger_id: str, ledger: LedgerPut, existing_ledgers):
    """Validate the incoming ledger has a unique name"""

    for ledger in existing_ledgers:
        if ledger['ledgerId'] == ledger_id:
            continue

        if ledger.glName:
            if ledger['glName'].lower() == ledger.glName.lower():
                return False
    return True

def check_missing_fields(dict_, required):
    """
    Check that the account information about to be updated does not input
    any null values for required fields
    """
    keys = list(dict_.keys())
    for field in REQUIRED_FIELDS:
        if field in keys:
            value = dict_[field]

            if value is None or value == '':
                return field
    
    return None
