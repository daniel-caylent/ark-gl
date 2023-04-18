import json

def response(code, context, data=None, **kwargs):
    response_ = {
        'statusCode': str(code),
        'eventId': context.aws_request_id,
        **kwargs
    }

    if data is not None:
        response_['body'] = data
    
    return response_
