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
        except Exception:
            return response(503, context.aws_request_id, detail="Internal Server Error.")
            

    return wrapper