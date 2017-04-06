import logging

from .builders import MessageBuilder
from .mixins import LoggingHelperMixin

__all__ = ['MessageAdapter', 'StrictMessageAdapter', 'LoggingAdapter', 'StrictLoggingAdapter']


class MessageAdapter(logging.LoggerAdapter):
    def __init__(self, logger, *args, **kwargs):
        self.kwargs = dict()
        super(MessageAdapter, self).__init__(logger, {})

    def info(self, message=None, *args, **kwargs):
        message = self.process(message, kwargs)
        self.logger.info(message)

    def debug(self, message=None, *args, **kwargs):
        message = self.process(message, kwargs)
        self.logger.debug(message)

    def exception(self, message=None, *args, **kwargs):
        message = self.process(message, kwargs)
        self.logger.exception(message)

    def process(self, message, kwargs):
        message_type = kwargs.pop('message_type')
        self.kwargs = kwargs
        message_builder = getattr(message_type, 'builder', MessageBuilder)
        return message_builder(message, message_type, self, **kwargs)


class StrictMessageAdapter(MessageAdapter):
    """
    Suppresses the custom log message
    """

    def process(self, message, kwargs):
        return super(StrictMessageAdapter, self).process(None, kwargs)


class LoggingAdapter(MessageAdapter, LoggingHelperMixin):
    pass


class StrictLoggingAdapter(StrictMessageAdapter, LoggingHelperMixin):
    pass
