from django.db import models

from common.utils.date_ops import DateTimeOperations as DtOps

__all__ = ['DefaultTZDateTimeField', 'CurrencyField']


class DefaultTZDateTimeField(models.DateTimeField):
    """
    A datetime field that returns db datetime values in the timezone provided in django settings
    """

    def from_db_value(self, value, expression, connection, context):
        """
        This method is used by django to parse model data to pythonic return data.
        If this is not defined, the default method "to_python" defined in the ModelField is used.
        """
        if value is None:
            return value

        return DtOps.to_default_timezone(value)


class CurrencyField(models.FloatField):
    """
    Field to be used to save currency values.
    All numeric values are rounded off to 2 decimal places before being saved to db
    """

    def get_prep_value(self, value):
        """
        This method is used by django to convert python values to db storage values.
        Perform preliminary non-db specific value checks and conversions.
        :param value: value is the current value of the model’s attribute, and the method should
                    return data in a format that has been prepared for use as a parameter in a query.
        """
        value = super(CurrencyField, self).get_prep_value(value)
        if value is None:
            return None
        return float('{0:.2f}'.format(value))
