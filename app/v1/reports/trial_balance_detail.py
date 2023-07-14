import datetime

from arkdb import reports, ledgers, accounts, account_attributes
from shared import endpoint, dataclass_error_to_str

from models import ReportInputs


@endpoint
def handler(event, context) -> tuple[int, dict]:
    """Handler for the trial balance report

    event: dict
    POST event passed in from API gateway. The key 'body' should
    cary the POST request as a JSON string

    context: LambdaContext
    Context about the instance of the lambda function

    """
    if not event.get("queryStringParameters"):
        return 400, {"detail": "Missing query parameters"}

    try:
        valid_input = ReportInputs(**event.get("queryStringParameters"))
    except Exception as e:
        return 400, {"detail": dataclass_error_to_str(e)}

    if valid_input.ledgerIds:
        for id_ in valid_input.ledgerIds:
            ledger = ledgers.select_by_id(id_)
            if ledger is None:
                return 400, {"detail": f"Invalid ledgerId: {id_}"}

    if valid_input.accountIds:
        for id_ in valid_input.accountIds:
            account = accounts.select_by_id(id_)
            if account is None:
                return 400, {"detail": f"Invalid accountId: {id_}"}

    if valid_input.attributeIds:
        for id_ in valid_input.attributeIds:
            attribute = account_attributes.select_by_id(id_)
            if attribute is None:
                return 400, {"detail": f"Invalid attributeId: {id_}"}


    lines = reports.get_trial_balance(valid_input.__dict__)

    report = {
        "decimals": None,
        "currencyName": None,
        "accounts": [],
        "lineItems": []
    }

    if lines:
        report["decimals"] = lines[0]["decimals"]
        report["currency"] = lines[0]["currency"]
        accounts_ = {}
        line_items = []
        for line in lines:
            if not accounts_.get(line["accountId"]):
                accounts_[line["accountId"]] = {
                    "total": line["amount"]
                }
            else:
                accounts_[line["accountId"]] += line["amount"]
            
            line_items.append({
                "ledgerName": line["ledgerName"],
                "ledgerId": line["ledgerId"],
                "accountId": line["accountId"],
                "entityId": line["entityId"],
                "journalEntryNum": line["journalEntryNum"],
                "date": line["journalEntryDate"],
                "adjustingJournalEntry": line["adjustingJournalEntry"],
                "memo": line["memo"],
                "state": line["journalEntryState"],
                "amount": line["amount"],
            })

        report["lineItems"] = line_items
        report["accounts"] = accounts_
    return 200, {"data": report}
