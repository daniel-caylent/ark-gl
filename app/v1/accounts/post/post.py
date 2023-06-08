"""Lambda that will perform POST requests for Accounts"""

import json
"""Lambda that will perform POST requests for Accounts"""

# pylint: disable=import-error; Lambda layer dependency
from arkdb import accounts
from shared import endpoint
from validate_new_account import validate_new_account
# pylint: enable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]:
    """Handler for the accounts POST request

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

    code, detail, post = validate_new_account(body)

    if code != 201:
        return code, {"detail": detail}

    # insert the new account
    result = accounts.create_new(post)
    return code, {"accountId": result}
