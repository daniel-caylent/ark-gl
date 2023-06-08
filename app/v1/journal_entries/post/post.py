"""
This Lambda is responsible for serving the journal entries POST request
"""
import json

 # pylint: disable=import-error; Lambda layer dependency
from arkdb import journal_entries
from validate_new_journal_entry import validate_new_journal_entry
from shared import endpoint
# pylint: enable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters
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
    except Exception: # pylint: disable=broad-exception-caught; Unhandled exception is not allowed
        return 400, {"detail": "Body does not contain valid json."}

    code, detail, post = validate_new_journal_entry(body)

    if code != 201:
        return code, {"detail": detail}

    # insert the new account
    result = journal_entries.create_new(post)
    return code, {"journalEntryId": result}
