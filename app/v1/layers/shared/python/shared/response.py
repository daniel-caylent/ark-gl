from .dataclass_encoder import encode

def response(code: int, id: str, data=None, **kwargs):
    """
    Generate json encodable and consistent responses for lambda functions

    code: 
    """

    response_ = {
        'statusCode': code,
        'eventId': id,
        **kwargs
    }

    if data is not None:
        response_['body'] = encode(data)

    return response_
