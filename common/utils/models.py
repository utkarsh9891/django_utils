from django.db import models

from common.utils.model_fields import DefaultTZDateTimeField

__all__ = ['MetaDataModel']


class MetaDataModel(models.Model):
    """
    Base model to be inherited across the project
    """
    created_by = models.CharField(max_length=100, default='NA')
    modified_by = models.CharField(max_length=100, default='NA')
    created_at = DefaultTZDateTimeField(auto_now_add=True)
    modified_at = DefaultTZDateTimeField(auto_now=True)

    class Meta:
        abstract = True
