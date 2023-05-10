import json

from .dataclass_encoder import encode


def response(code: int, id: str, data=None, **kwargs):
    """
    Generate json encodable and consistent responses for lambda functions

    code: 
    """

    response_ = {
        'statusCode': code,
        'isBase64Encoded': False,
    }

    body = {
        'eventId': id,
        'statusCode': code,
        **kwargs
    }

    if data is not None:
        body['data'] = encode(data)

    response_['body'] = json.dumps(body)
    return response_
