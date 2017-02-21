import logging

import requests
from common.external_apis import check_perm_url
from common.utils import print_exception
from django.conf import settings

from common.utils.vars import forbidden, failure, success

logger = logging.getLogger('django_utils.request')


class EnableACLMixin:
    # Dummy action_acl_map -- should be overridden in all inheriting ViewSets
    action_acl_map = {
        'retrieve': {'object_type': 'model', 'action': 'retrieve'},
        'create': {'object_type': 'model', 'action': 'create'},
        'update': {'object_type': 'model', 'action': 'update'}
    }

    @staticmethod
    def check_permission_from_acl(user_id=None, store_id=None, object_type='', acl_action='', object_owner=''):
        allowed_status = forbidden
        try:
            request_data = {
                'user_id': user_id,
                'store_id': store_id,
                'permission': {
                    'module': settings.SELF_MODULE_SLUG,
                    'object_type': object_type,
                    'action': acl_action
                }
            }
            if object_owner:
                request_data['object_owner'] = object_owner

            acl_response = requests.post(check_perm_url, json=request_data)
            if acl_response.ok and acl_response.json().get('is_allowed'):
                allowed_status = success

        except:
            print_exception()
            allowed_status = failure

        if allowed_status is not success:
            logger.warn('Permission validation failed with status code {}'.format(allowed_status))

        return allowed_status

    def check_permissions(self, request):
        super(EnableACLMixin, self).check_permissions(request)
        user_id = request.META.get('HTTP_USER_ID')
        action_acl_permission = self.action_acl_map.get(self.action)

        if action_acl_permission:
            request_dict = request.query_params.dict() if request.method == 'GET' else request.data
            param_store_id = request_dict.get('store_id')
            store_id = param_store_id or request.META.get('HTTP_STORE_ID')
            request.store_id = store_id or 'NA'
            action_allowed = self.check_permission_from_acl(user_id=user_id, store_id=store_id,
                                                            object_type=action_acl_permission['object_type'],
                                                            acl_action=action_acl_permission['acl_action'])
        else:
            action_allowed = success

        if action_allowed is not success:
            denied_message = 'You do not have permission for the requested action. Please contact your admin.'
            self.permission_denied(request, message=denied_message)

        request.user_id = user_id or 'NA'

    def handle_exception(self, exc):
        response = super(EnableACLMixin, self).handle_exception(exc)
        resp_dict = response.data
        if not resp_dict.get('message') and resp_dict.get('detail'):
            resp_dict['message'] = resp_dict['detail']
            resp_dict.pop('detail')
            response.data = resp_dict

        return response
