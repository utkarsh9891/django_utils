from collections import namedtuple

from .builders import MessageBuilder

__all__ = ['SYSTEM_IN', 'SYSTEM_OUT', 'EXCEPTION', 'API_IN_WITH_DATA', 'API_OUT_WITH_DATA', 'API_IN', 'API_OUT']

MESSAGE_TYPE = namedtuple('MESSAGE_TYPE', 'format builder')

MESSAGE_TYPE.__new__.__defaults__ = (MessageBuilder,)

SYSTEM_IN = MESSAGE_TYPE(
    format='SYSTEM_IN {request_path}'
)

SYSTEM_OUT = MESSAGE_TYPE(
    format='SYSTEM_OUT {request_path} {response_code} {processing_time}'
)

EXCEPTION = MESSAGE_TYPE(
    format='EXCEPTION {request_path}\nexception:{message}'
)

API_IN_WITH_DATA = MESSAGE_TYPE(
    format='API_IN_WITH_DATA {request_method} {request_path} {request_client_ip}\n'
           'api_action<{api_action}> {request_data}'
)

API_OUT_WITH_DATA = MESSAGE_TYPE(
    format='API_OUT_WITH_DATA {request_method} {request_path} {request_client_ip} {response_code}\n'
           'api_action<{api_action}> {response_data}'
)

API_IN = MESSAGE_TYPE(
    format='API_IN {request_method} {request_path} api_action<{api_action}>'
)

API_OUT = MESSAGE_TYPE(
    format='API_OUT {request_path} {response_code} api_action<{api_action}>'
)
