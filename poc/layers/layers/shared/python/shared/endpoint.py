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
            result = func_with_logging(event, context)

            return result
        except Exception:
            return response(503, context)
            

    return wrapper