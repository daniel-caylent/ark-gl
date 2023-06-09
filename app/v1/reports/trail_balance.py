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

    ledger_id = event["pathParameters"].get("ledgerIds", None)
    if ledger_id is None:
        return 400, {"detail": "No ledger specified."}
    
    start_date = event["pathParameters"].get("startDate", None)
    end_date = event["pathParameters"].get("endDate", None)
    state = event["pathParameters"].get("journalEntryState", None)
    balance = event["pathParameters"].get("hideZeroBalance", None)

