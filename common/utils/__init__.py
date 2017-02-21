import linecache
import sys
import traceback
from functools import reduce
from operator import __or__ as OR

import arrow
from decorator import decorator
from django.conf import settings
from django.db.models import Q

from django_utils.common.utils.vars import unauthorized
from .hr import hr


def get_month_range(month, year):
    """
    get the range of timestamp for beginning & end of month
    :param month: the month for the range
    :param year: year for range
    :return: the start & end timestamp of the month
    """
    arr = arrow.get(year, month, 15, tzinfo=settings.TIME_ZONE)
    first_day, last_day = arr.span('month')
    return first_day.datetime, last_day.datetime


# http://stackoverflow.com/a/20264059/2422840
def print_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN:\nFILE:{}\nLINE No. {}\nLINE:"{}"\nERROR:{}'.format(
        filename, lineno, line.strip(), exc_obj))
    hr('-')


@decorator
def print_error(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        traceback_text = ''.join(traceback.format_exception(*sys.exc_info()))
        print('EXCEPTION IN:\nFUNCTION: {}\nERROR: {}\nEXCEPTION: {}'.format(
            fn.__name__, exc_obj, traceback_text))
        hr('-')


def filtered_data(**kwargs):
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
    accounts = kwargs.get('accounts', False)
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


def get_date_filter(lookup_timestamp, include_null_start=True, start_field='start_date', end_field='end_date'):
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


def stringify_serializer_errors(serializer):
    """
    Stringify the errors in the serializer error dict to a single string
    :param serializer: the serializer object
    :return: the stringified serializer errors
    """
    return '; '.join(['{} -- {}'.format(key, value[0]) for key, value in serializer.errors.items()])


def exception_msg(e):
    if hasattr(e, 'messages'):
        return '; '.join(e.messages)
    elif hasattr(e, 'msg'):
        return str(e.msg)
    else:
        return str(e)


def parse_request_dict(request_dict, params_map):
    """
    Parses a request & retrieves the parameters as per the params mapping
    :param request_dict: the django request dictionary -- request.data or request.query_params.dict() or request.META
    :param params_map: the map for the arguments to be retrieved. Consists of tuples of structure
    (<param_name>, <param_type>, <default>)
    OR
    ((<param_from_name>, <param_to_name>), <param_type>, <default>)

    [
        ('store_id', int, None),
        (('product_price', 'price'), float, 0),
        ('order_date', DtOps.ist_datetime, None),
        ('store_name', str, '')
    ]

    If default is not defined in any tuple & the item is not found, it is not added to the resultant dictionary
    :return: the dict of params
    """
    result_params = {}
    if not isinstance(request_dict, dict):
        return result_params

    for param_map in params_map:
        if len(param_map) == 2:
            has_default = False
            param_default = None
            param_name, param_type = param_map
        else:
            has_default = True
            param_name, param_type, param_default = param_map

        if isinstance(param_name, tuple) or isinstance(param_name, list):
            to_name = param_name[1]
            param_name = param_name[0]
        else:
            to_name = param_name

        try:
            value = request_dict.get(param_name)
            if value is not None:
                if type(value) is str:
                    value = value.strip()
                result_params[to_name] = param_type(value)
            elif has_default:
                result_params[to_name] = param_default
        except:
            print_exception()
            # Invalid data type passed in for parameter value. Skip value assignment

    return result_params


def split_str(string, data_type=str):
    """
    Splits a comma separated string to an array of data type as specified by data_type
    :param string: the target comma separated string to split
    :param data_type: the target data type
    :return: an array for the split string
    """
    split_string = None
    if type(string) == str:
        split_string = string.split(',')

    if data_type is not str:
        split_string = [data_type(item) for item in split_string]

    return split_string


def flatten(lis):
    result = []
    for item in lis:
        if isinstance(item, list):
            result.extend(flatten(item))
        # won't accept empty dict or tuple
        elif item not in [None, (), {}]:
            result.append(item)
    return result


def get_model_display_fields(model_name, exclusion_list=None):
    exclusion_list = exclusion_list or []
    # List of all concrete model fields, except for the relational fields
    all_list_fields = [f.name for f in model_name._meta.get_fields() if f.concrete and not (
        f.is_relation or f.one_to_one or f.many_to_one or f.related_model)]

    return list(set(all_list_fields) - set(exclusion_list))
