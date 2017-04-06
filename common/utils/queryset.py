from functools import reduce
from operator import __or__ as OR

from django.db.models import Q

__all__ = ['QuerysetHelpers']


class QuerysetHelpers:
    """
    Django specific utility functions that can be used across all projects
    """

    @classmethod
    def query_data(cls, **kwargs):
        """
        Returns the queryset of the specified model, along with the filters & exclusions applied
        """
        model = kwargs.get('model')
        queryset = kwargs.get('queryset')
        filter_args = kwargs.get('filter_args', [])
        filter_kwargs = kwargs.get('filter_kwargs', {})
        exclude_args = kwargs.get('exclude_args', [])
        exclude_kwargs = kwargs.get('exclude_kwargs', {})
        values = kwargs.get('values', [])
        values_list = kwargs.get('values_list', [])
        order_by = kwargs.get('order_by', [])
        using = kwargs.get('using')

        if any([model, queryset]) is False:
            return

        if model:
            if using:
                source = model.objects.using(using)
            else:
                source = model.objects
        else:
            source = queryset

        queryset = source.filter(*filter_args, **filter_kwargs).exclude(*exclude_args, **exclude_kwargs)
        if order_by:
            queryset = queryset.order_by(*order_by)

        if values:
            return queryset.values(*values)

        if values_list:
            return list(queryset.values_list(*values_list, flat=True))

        return queryset

    @classmethod
    def get_date_filter(cls, lookup_timestamp, include_null_start=True, start_field='start_date', end_field='end_date'):
        """
        Query to get configs which are valid at the lookup timestamp
        :param lookup_timestamp: the timestamp for lookup
        :param include_null_start: whether "NULL, NULL" & "NULL, <date>" as "start, end" combination is to be included
                                 By default, it would be included as a valid case
        :param start_field: the start date field in model
        :param end_field: the end date field in model
        :return: filter kwargs for the date range
        """
        start_is_null = '{}__isnull'.format(start_field)
        end_is_null = '{}__isnull'.format(end_field)
        start_lte = '{}__lte'.format(start_field)
        end_gte = '{}__gte'.format(end_field)

        date_filter = [Q(**{start_lte: lookup_timestamp, end_is_null: True}),
                       Q(**{start_lte: lookup_timestamp, end_gte: lookup_timestamp})]

        if include_null_start:
            date_filter.extend([
                Q(**{start_is_null: True, end_is_null: True}),
                Q(**{start_is_null: True, end_gte: lookup_timestamp})
            ])

        # Source: http://simeonfranklin.com/blog/2011/jun/14/best-way-or-list-django-orm-q-objects/
        date_filter = reduce(OR, date_filter)

        return date_filter

    @classmethod
    def stringify_serializer_errors(cls, serializer):
        """
        Stringify the errors in the serializer error dict to a single string
        :param serializer: the serializer object
        :return: the stringified serializer errors
        """
        return '; '.join(['{} -- {}'.format(key, value[0]) for key, value in serializer.errors.items()])
