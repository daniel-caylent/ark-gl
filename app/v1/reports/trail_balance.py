from arkdb import reports
from shared import endpoint

@endpoint
def handler(event, context) -> tuple[int, dict]:
    """Handler for the trial balance report

    event: dict
    POST event passed in from API gateway. The key 'body' should
    cary the POST request as a JSON string

    context: LambdaContext
    Context about the instance of the lambda function
    
    """
    if not event.get("pathParameters"):
        return 400, {"detail": "Missing path parameters"}

    inputs = {
        "startDate": event["pathParameters"].get("startDate"),
        "endDate": event["pathParameters"].get("endDate"),
        "journalEntryState": event["pathParameters"].get("journalEntryState"),
        "hideZeroBalance": event["pathParameters"].get("hideZeroBalance"),
        "ledgerId": event["pathParameters"].get("ledgerId")
    }

    report = reports.get_trial_balance(ledger_ids, state, start_date, end_date, hide_zero_balance)

    return 200, {data: report}