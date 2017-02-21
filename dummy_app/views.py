from rest_framework import viewsets
from rest_framework.response import Response

from common.logging.mixins import APILoggingMixin
from common.utils.vars import success


class LoggingDemoViewSet(APILoggingMixin, viewsets.GenericViewSet):
    def list(self, request):
        response_dict = {'message': 'This is a dummy response message'}
        return Response(response_dict, success)
