from common.utils import get_model_display_fields
from django.db import models

from common.fields import DefaultTZDateTimeField


class MetaDataModel(models.Model):
    created_by = models.CharField(max_length=100, default='NA')
    modified_by = models.CharField(max_length=100, default='NA')
    created_at = DefaultTZDateTimeField(auto_now_add=True)
    modified_at = DefaultTZDateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def display_data(self, exclusion_list=None):
        exclusion_list = exclusion_list or []
        exclude_fields = ['created_by', 'created_at', 'modified_by', 'modified_at'] + exclusion_list

        temp = {f: getattr(self, f) for f in get_model_display_fields(
            model_name=self.__class__, exclusion_list=exclude_fields)}
        return temp
