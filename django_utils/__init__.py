import os


def get_var(variable_name, default=None):
    """ method to raise exception if some environment variable is not set"""
    val = os.environ.get(variable_name, default)
    if val is None:
        raise EnvironmentError(
            'Please set the environment variable {0}'.format(variable_name))
    return val
