from functools import wraps
import logging
import json
import os
import sys
import traceback

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'ERROR').upper()
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

def use_logging(func):
    """
    Wrapper to run a function with good logging for lambda functions
    """
    @wraps(func)
    def wrapper(event, context):
        logger.info(f'event: {event}')
        logger.info(f'context: {context}')

        try:
            result = func(event, context)
            return result

        except Exception:
            exception_type, exception_value, exception_traceback = sys.exc_info()
            traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
            err_msg = json.dumps({
                'errorType': exception_type.__name__,
                'errorMessage': str(exception_value),
                'stackTrace': traceback_string
            })
            logger.error(f'event: {event}')
            logger.error(f'context: {context}')
            logger.error(err_msg)

            raise Exception(err_msg)
    
    return wrapper
