import datetime

from arkdb import reports, ledgers
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

    inputs = {
        "startDate": event["queryStringParameters"].get("startDate"),
        "endDate": event["queryStringParameters"].get("endDate"),
        "journalEntryState": event["queryStringParameters"].get("journalEntryState"),
        "ledgerId": event["queryStringParameters"].get("ledgerId")
    }

    try:
        valid_input = ReportInputs(**inputs)
    except Exception as e:
        return 400, {"detail": dataclass_error_to_str(e)}

    for id_ in valid_input.ledgerId:
        ledger = ledgers.select_by_id(id_)
        if ledger is None:
            return 400, {"detail": f"Invalid ledger ID: {id_}"}

    report = reports.get_trial_balance(valid_input.__dict__)

    for line in report:
        line["je_date"] = str(line["je_date"])
        line["je_post_date"] = str(line["je_post_date"])

    return 200, {"data": report}
