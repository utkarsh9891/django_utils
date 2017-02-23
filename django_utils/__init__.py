import os


def get_var(variable_name, default=None):
    """
    Retrieves the value of an environment variable.
    If the variable is not set and no default is given, an EnvironmentError exception is raised
    :param variable_name: the variable to be retrieved
    :param default: the default value if not found
    :return: the value of the env variable or default
    """
    val = os.environ.get(variable_name, default)
    if val is None:
        raise EnvironmentError(
            'Please set the environment variable {0}'.format(variable_name))
    return val
