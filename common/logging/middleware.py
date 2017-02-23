import logging
import time

from . import message_types
from .adapters import LoggingAdapter

logger = LoggingAdapter(logging.getLogger(__name__))


class LoggingMiddleware:
    """
    Import this middleware class into the MIDDLEWARE_CLASSES django setting.
    Should be placed after CommonMiddleware and SessionMiddleware so that appropriate request
        parameters are setup before this middleware runs.
    """

    def __init__(self):
        self.time_in = None

    def process_request(self, request):
        self.time_in = time.time()
        logger.info(message_type=message_types.SYSTEM_IN, request=request)

    def process_response(self, request, response):
        logger.info(message_type=message_types.SYSTEM_OUT, request=request, response=response,
                    processing_time=time.time() - self.time_in)
        return response


class ExceptionLoggingMiddleware:
    """
    Import this middleware to log exceptions in custom manner within django logs
    """

    def process_exception(self, request, exception):
        logger.exception(exception, message_type=message_types.EXCEPTION, request=request)
