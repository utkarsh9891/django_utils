import linecache
import logging
import sys

__all__ = ['ExceptionLogger']
logger = logging.getLogger(__name__)


class ExceptionLogger:
    # http://stackoverflow.com/a/20264059/2422840
    @staticmethod
    def print_exception():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        error_details = 'EXCEPTION IN:\nFILE:{}\nLINE No. {}\nLINE:"{}"\nERROR:{}'.format(
            filename, lineno, line.strip(), exc_obj)
        print(error_details)

    @staticmethod
    def log_exception(logger):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        error_details = 'EXCEPTION IN:\nFILE:{}\nLINE No. {}\nLINE:"{}"\nERROR:{}'.format(
            filename, lineno, line.strip(), exc_obj)
        logger.error(error_details)

    @staticmethod
    def print_and_log_exception(logger):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        error_details = 'EXCEPTION IN:\nFILE:{}\nLINE No. {}\nLINE:"{}"\nERROR:{}'.format(
            filename, lineno, line.strip(), exc_obj)
        print(error_details)
        logger.error(error_details)
