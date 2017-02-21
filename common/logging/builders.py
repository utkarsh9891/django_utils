import string


class MessageBuilder(string.Formatter):
    """
    String formatter for log message string
    """

    # The key to be used for message text in message builders.
    # For other items, getters would be defined e.g. request_data would have a function get_request_data in subclass
    MESSAGE_KEY_NAME = 'message'

    def __init__(self, message, message_type, adapter, *args, **kwargs):
        # The message string to be logged
        self.message = message
        # The contextual message format to be used for generating log message
        self.message_type_format = message_type.format
        # The logging adapter to be used for specifying contextual information in logging output
        self.message_adapter = adapter
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.format(self.message_type_format)

    def get_value(self, key, args, kwargs):
        if isinstance(key, int):
            return ''

        if key == self.MESSAGE_KEY_NAME:
            return self.message if self.message else ''

        try:
            return getattr(self.message_adapter, 'get_%s' % key.lower())()
        except AttributeError:
            return self.kwargs.get(key, self.message_adapter.DEFAULT_VALUE)
