from django.conf import settings

ACCOUNTS_HOST_NAME = settings.ACCOUNTS_HOST_NAME

check_perm_url = ACCOUNTS_HOST_NAME + '/acl/user/check-permission/'
