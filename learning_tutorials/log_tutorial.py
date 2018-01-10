import logging


# Create module level logger
module_logger = logging.getLogger('uscc_eng_parser_api.' + __name__)


class MyApp:
    """

    """
    def __init__(self):
        module_logger.info('creating an instance of MyApp')

    def app_function(self):
        """

        :return:
        """
        module_logger.info('performing application functionality')
        a = 1 + 1
        module_logger.critical("application encountered a critical error")


def some_module_function():
    module_logger.info('received a call to this function. %s', 'Passing variable data as part of the logging')
