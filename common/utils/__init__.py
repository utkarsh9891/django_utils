import linecache
import sys

from common.utils.vars import unauthorized


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


def parse_dict(request_dict, params_map):
    """
    Parses a dictionary & retrieves the parameters as per the params mapping
    :param request_dict: the dictionary to be parsed -- request.data or request.query_params.dict() or request.META
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
