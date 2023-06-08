"""Standard logging module"""

from functools import wraps
import logging
import json
import os
import sys
import traceback
import datetime
import time

LOG_LEVEL = os.environ.get("LOG_LEVEL", "ERROR").upper()
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


def use_logging(func):
    """
    Wrapper to run a function with good logging for lambda functions
    """

    @wraps(func)
    def wrapper(event, context):
        logger.info(f"event: {event}")
        logger.info(f"context: {context}")

        try:
            result = func(event, context)
            return result

        except Exception:
            exception_type, exception_value, exception_traceback = sys.exc_info()
            traceback_string = traceback.format_exception(
                exception_type, exception_value, exception_traceback
            )
            err_msg = json.dumps(
                {
                    "errorType": exception_type.__name__,
                    "errorMessage": str(exception_value),
                    "stackTrace": traceback_string,
                }
            )
            logger.error(f"event: {event}")
            logger.error(f"context: {context}")
            logger.error(err_msg)

            write_log(event, context, "Warning", "API", err_msg)
            raise Exception(err_msg)

    return wrapper


def write_log(event, context, severity: str, alert_type: str, alert_message: str):
    """Write a standardized error message"""

    func_dict = {
        "Emergency": logger.error,
        "Alert": logger.warning,
        "Critical": logger.critical,
        "Warning": logger.warning,
        "Notice": logger.info,
        "Informational": logger.info,
        "Debug": logger.debug,
    }

    logging_func = func_dict.get(severity)
    if logging_func is None:
        logging_func = logger.info

    message_dump = json.dumps(
        {
            "ark-alert-event": {
                "eventId": context.aws_request_id,
                "traceId": None,
                "alertTimeUTC": datetime.datetime.now().isoformat(),
                "alertTimeEpoch": time.mktime(datetime.datetime.now().timetuple()),
                "serviceType": "Lambda",
                # "serviceName": "(name of service or API) --> CreateAccount",
                "serviceArn": context.invoked_function_arn,
                "severity": severity,
                "alertDetail": {
                    "alertType": alert_type,
                    "alertMessage": alert_message,
                },
            }
        }
    )

    logging_func(message_dump)
