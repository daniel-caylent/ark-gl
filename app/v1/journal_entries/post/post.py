import json

from arkdb import journal_entries  # pylint: disable=import-error
from validate_new_journal_entry import validate_new_journal_entry
from shared import endpoint


@endpoint
def handler(event, context) -> tuple[int, dict]:
    """Handler for the journal entries POST request

    event: dict
    POST event passed in from API gateway. The key 'body' should
    cary the POST request as a JSON string

    context: LambdaContext
    Context about the instance of the lambda function
    """

    # validate the request body
    try:
        body = json.loads(event["body"])
    except:
        return 400, {"detail": "Body does not contain valid json."}

    code, detail, post = validate_new_journal_entry(body)

    if code != 201:
        return code, {"detail": detail}

    # insert the new account
    result = journal_entries.create_new(post)
    return code, {"journalEntryId": result}
