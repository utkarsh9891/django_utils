import json as json_lib
import logging

from common.utils import get_caller_logger

__all__ = ['LoggedRequests', 'PatchedRequests']

logger = logging.getLogger(__name__)


class RequestLogger:
    @classmethod
    def log_request(cls, request_type, url, params=None, data=None, json=None, log_title=None, **kwargs):
        log_message = log_title or ''
        log_message += 'Triggered {request_type} on {url}:'.format(request_type=request_type.upper(), url=url)

        if params is not None:
            log_message += '\nPARAMS: {}'.format(json_lib.dumps(params, sort_keys=True))
        if data is not None:
            log_message += '\nDATA: {}'.format(data)
        if json is not None:
            log_message += '\nJSON: {}'.format(json_lib.dumps(json, sort_keys=True))

        headers = kwargs.get('headers')
        if headers is not None:
            log_message += '\nHEADERS: {}'.format(json_lib.dumps(headers, sort_keys=True))

        auth = kwargs.get('auth')
        if auth is not None:
            log_message += '\nAUTH: {}'.format(json_lib.dumps(auth))

        logger_to_use = get_caller_logger(stack_depth=2, default_logger=logger)
        logger_to_use.info(log_message)
        print(log_message)

    @classmethod
    def log_response(cls, request_type, url, response, log_response_data=True, log_title=None):
        log_message = log_title or ''
        log_message += 'Response for {request_type} on {url}:\nSTATUS: {status}'.format(
            request_type=request_type.upper(), url=url, status=response.status_code)

        if log_response_data:
            log_message += '\nCONTENT: {}'.format(response.content)

        logger_to_use = get_caller_logger(stack_depth=2, default_logger=logger)
        logger_to_use.info(log_message)
        print(log_message)

    @classmethod
    def log_request_response(cls, request_type):
        def log_decorator(request_func):
            def request_func_wrapper(_cls, url, log_response_data=True, log_title=None, *args, **kwargs):
                RequestLogger.log_request(request_type=request_type, url=url, log_title=log_title, *args, **kwargs)
                response = request_func(_cls, url, *args, **kwargs)
                RequestLogger.log_response(request_type=request_type, url=url, response=response,
                                           log_response_data=log_response_data, log_title=log_title)
                return response

            return request_func_wrapper

        return log_decorator

    @classmethod
    def log_request_response_patched(cls, request_type):
        def log_decorator(request_func):
            def request_func_wrapper(_cls, url, log_response_data=True, log_title=None, vanilla=False, *args, **kwargs):
                if not vanilla:
                    RequestLogger.log_request(request_type=request_type, url=url, log_title=log_title, *args, **kwargs)
                response = request_func(_cls, url, *args, **kwargs)
                if not vanilla:
                    RequestLogger.log_response(request_type=request_type, url=url, response=response,
                                               log_response_data=log_response_data, log_title=log_title)
                return response

            return request_func_wrapper

        return log_decorator


class LoggedRequests:
    @classmethod
    @RequestLogger.log_request_response('get')
    def get(cls, url, params=None, **kwargs):
        from requests import get
        response = get(url=url, params=params, **kwargs)
        return response

    @classmethod
    @RequestLogger.log_request_response('post')
    def post(cls, url, data=None, json=None, **kwargs):
        from requests import post
        response = post(url=url, data=data, json=json, **kwargs)
        return response

    @classmethod
    @RequestLogger.log_request_response('patch')
    def patch(cls, url, data=None, **kwargs):
        from requests import patch
        response = patch(url=url, data=data, **kwargs)
        return response

    @classmethod
    @RequestLogger.log_request_response('put')
    def put(cls, url, data=None, **kwargs):
        from requests import put
        response = put(url=url, data=data, **kwargs)
        return response

    @classmethod
    @RequestLogger.log_request_response('delete')
    def delete(cls, url, **kwargs):
        from requests import delete
        response = delete(url=url, **kwargs)
        return response

    @classmethod
    @RequestLogger.log_request_response('options')
    def options(cls, url, **kwargs):
        from requests import options
        response = options(url=url, **kwargs)
        return response


class PatchedRequests:
    @classmethod
    @RequestLogger.log_request_response_patched('get')
    def get(cls, url, params=None, **kwargs):
        from requests import request
        kwargs.setdefault('allow_redirects', True)
        response = request('get', url, params=params, **kwargs)
        return response

    @classmethod
    @RequestLogger.log_request_response_patched('post')
    def post(cls, url, data=None, json=None, **kwargs):
        from requests import request
        response = request('post', url, data=data, json=json, **kwargs)
        return response

    @classmethod
    @RequestLogger.log_request_response_patched('patch')
    def patch(cls, url, data=None, **kwargs):
        from requests import request
        response = request('patch', url, data=data, **kwargs)
        return response

    @classmethod
    @RequestLogger.log_request_response_patched('put')
    def put(cls, url, data=None, **kwargs):
        from requests import request
        response = request('put', url, data=data, **kwargs)
        return response

    @classmethod
    @RequestLogger.log_request_response_patched('delete')
    def delete(cls, url, **kwargs):
        from requests import request
        response = request('delete', url, **kwargs)
        return response

    @classmethod
    @RequestLogger.log_request_response_patched('options')
    def options(cls, url, **kwargs):
        from requests import request
        kwargs.setdefault('allow_redirects', True)
        response = request('options', url, **kwargs)
        return response

    @classmethod
    def patch_library(cls):
        import requests
        requests.get = cls.get
        requests.post = cls.post
        requests.patch = cls.patch
        requests.put = cls.put
        requests.delete = cls.delete
        requests.options = cls.options
