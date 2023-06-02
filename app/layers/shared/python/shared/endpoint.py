from functools import wraps

from .response import response
from .logging import use_logging

def endpoint(func):
    """
    Decorator used to enable logging and error catch/response for lambda APIs
    """
    @wraps(func)
    def wrapper(event, context):
        try:
            func_with_logging = use_logging(func)
            code, data = func_with_logging(event, context)

            return response(code, context.aws_request_id, **data)
        except Exception as e:
            return response(500, context.aws_request_id, detail=f"Internal Server Error")


    return wrapper
