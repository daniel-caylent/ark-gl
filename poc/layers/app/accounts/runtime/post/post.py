import json

from models import AccountPost
from shared import endpoint


@endpoint
def handler(event, context):
    fund_id = event['queryStringParameters'].get('fundId', None)
    if fund_id is None:
        return 400, {'detail': "No fund specified."}

    body = json.loads(event.body)

    # validate the POST body
    try:
        post = AccountPost(**body)
    except:
        return 400, {'detail': "Body does not contain valid data."}
    
    # attribute must belong to client & fund
    # no inactive attributes ??? does this refer to /account-attributes? Those should be global...

    # try to insert the account
    try:
        # result = account_post(post.__dict__)
        result = 'a-unique-account-id'
    except Exception as e:
        return 400, {'detail': f"Failed to insert account due to: {str(e)}"}

    return 200, {'accountId': result}
