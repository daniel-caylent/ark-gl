"""Module that defines a decorator for all lambdas that serve the API Gateway"""

from functools import wraps
import os
import cProfile as profile
import pstats
import traceback

from .response import response
from .logging import use_logging


def endpoint(func):
    """
    Decorator used to enable logging and error catch/response for lambda APIs
    """

    @wraps(func)
    def wrapper(event, context):
        profiling = os.getenv("PROFILE")
        func_with_logging = use_logging(func)

        if profiling:
            profile.runctx('func_with_logging(event, context)', globals(), locals(), '/tmp/profile-stats')
            p = pstats.Stats('/tmp/profile-stats')
            p.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(50)
            return response(200, context.aws_request_id, {"Detail": "Check CloudWatch log for profile results."})

        try:
            code, data = func_with_logging(event, context)
            return response(code, context.aws_request_id, **data)

        except Exception as e:
            print(traceback.format_exc())
            return response(
                500, context.aws_request_id, detail=f"Internal Server Error: {str(e)}"
            )

    return wrapper
