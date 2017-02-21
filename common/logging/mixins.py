import json
import logging

from . import message_types


class LoggingHelperMixin:
    DEFAULT_VALUE = 'NA'

    def __init__(self, *args, **kwargs):
        self.kwargs = dict()

    @staticmethod
    def __new__(cls, *more):
        if cls is LoggingHelperMixin:
            raise TypeError('Logging Helper Mixing may not be instantiated')
        return object.__new__(cls)

    def get_api_action(self):
        return self.kwargs.get('api_action', self.DEFAULT_VALUE)

    def get_user_id(self):
        return self.kwargs['request'].META.get('HTTP_USER_ID', self.DEFAULT_VALUE)

    def get_request_path(self):
        return self.kwargs['request'].path

    def get_session_id(self):
        return self.kwargs['request'].session.session_key or self.DEFAULT_VALUE

    def get_request_method(self):
        return self.kwargs['request'].method.upper()

    def get_request_client_ip(self):
        x_forwarded_for = self.kwargs['request'].META.get('HTTP_X_FORWARDED_FOR', None)
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0]
        else:
            client_ip = self.kwargs['request'].META.get('REMOTE_ADDR', None)
        return client_ip

    def get_request_data(self):
        request = self.kwargs.get('request', None)
        if not request:
            return 'NO_REQUEST_OBJECT_FOUND'

        header_keys = self.kwargs.get('header_keys', [])
        header_dict = {}
        if header_keys:
            for key in header_keys:
                header_dict[key] = request.META.get(key, None)
        else:
            for key, value in request.META.items():
                if key.startswith('HTTP_'):
                    header_dict[key] = value

        query_params = json.dumps(request.query_params.dict(), sort_keys=True)

        content_type = request.META.get('CONTENT_TYPE') or request.META.get('HTTP_CONTENT_TYPE', '')

        if 'multipart/form-data' in content_type:
            request_data = request.data.dict()
        else:
            request_data = request.data.copy()

        for filename in request.FILES:
            request_data[filename] = 'FILE[{}]'.format(request_data[filename].name)

        return 'HEADERS: {headers}, QUERY_PARAMS: {query_params}, REQUEST_DATA: {request_data}'.format(
            query_params=query_params,
            request_data=request_data,
            headers=json.dumps(header_dict, sort_keys=True)
        )

    def get_response_data(self):
        response_data = json.dumps(self.kwargs['response'].data, sort_keys=True)
        return 'RESPONSE: {}'.format(response_data)

    def get_response_code(self):
        return self.kwargs['response'].status_code


class APILoggingMixin:
    action = None
    # header keys to be logged. If this is not set or is empty, all HTTP_xxx headers are logged
    header_keys = []
    # ViewSet actions for which request data is not to be logged
    skip_response_data_actions = []
    # ViewSet actions for which response data is not to be logged
    skip_request_data_actions = []

    @staticmethod
    def __new__(cls, *more, **kwargs):
        if cls is APILoggingMixin:
            raise TypeError('Logging Mixing may not be instantiated')
        return super().__new__(cls)

    def initial(self, request, *args, **kwargs):
        from .adapters import LoggingAdapter
        super(APILoggingMixin, self).initial(request, *args, **kwargs)

        logger = LoggingAdapter(logging.getLogger(self.__module__))
        api_action = '{}.{}.{}'.format(self.__module__, self.__class__.__name__, self.action)

        if self.skip_request_data_actions and self.action in self.skip_request_data_actions:
            logger.info(message_type=message_types.API_IN, request=request, api_action=api_action)
        else:
            logger.info(message_type=message_types.API_IN_WITH_DATA, request=request, api_action=api_action,
                        header_keys=self.header_keys)

    def finalize_response(self, request, response, *args, **kwargs):
        from .adapters import LoggingAdapter
        response = super(APILoggingMixin, self).finalize_response(request, response, *args, **kwargs)

        logger = LoggingAdapter(logging.getLogger(self.__module__))
        api_action = '{}.{}.{}'.format(self.__module__, self.__class__.__name__, self.action)
        if self.skip_response_data_actions and self.action in self.skip_response_data_actions:
            logger.info(message_type=message_types.API_OUT, request=request, response=response, api_action=api_action)
        else:
            logger.info(message_type=message_types.API_OUT_WITH_DATA, request=request, response=response,
                        api_action=api_action)

        return response
