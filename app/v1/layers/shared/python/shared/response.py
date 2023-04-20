import json

from .json_encoder import EnhancedJSONEncoder

def response(code: int, id: str, data=None, **kwargs):
    """
    Generate json encodable and consistent responses for lambda functions

    code: 
    """

    response_ = {
        'statusCode': str(code),
        'eventId': id,
        **kwargs
    }

    if data is not None:
        response_['body'] = json.dumps(data, cls=EnhancedJSONEncoder)

    return response_
