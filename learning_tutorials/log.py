import argparse
import logging

from learning_tutorials.log_tutorial import MyApp
from learning_tutorials.log_tutorial import some_module_function


def main():
    """

    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--log')
    args = vars(parser.parse_args())
    logging_override = args.get('log')
    if logging_override is not None:
        parent_logger = logging_setup(logging_override)
    else:
        parent_logger = logging_setup()

    # numerical_log_level = getattr(logging, log_level.upper(), None)
    # if not isinstance(numerical_log_level, int):
    #     raise ValueError('Invalid log level: %s. Valid values are: %s' % (log_level,
    #                                                                       'DEBUG, INFO, WARNING, ERROR, or CRITICAL'))
    # logging.basicConfig(filename='example.log', filemode='w', level=numerical_log_level,
    #                     format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    # print(logging.getLogger().getEffectiveLevel())
    # print(logging.getLevelName(numerical_log_level))
    parent_logger.info("Logging facility established")
    parent_logger.info("creating instance of log_tutorial.myapp")
    app = MyApp()
    if isinstance(app, MyApp):
        parent_logger.info('successful creation of Myapp instance. Calling application functionality')
        app.app_function()
        parent_logger.info('finished application functionality')
        parent_logger.info('calling some_module_function()')
        some_module_function()
        parent_logger.error('some_module_function could not complete')
    else:
        parent_logger.error('MyApp can not be started. Shutting down.')
        return False

    return True


def logging_setup(log_level='INFO'):
    """
    Sets up parent logger object(api_logger), handlers (if any), and sets default formatters. This allows any child
    loggers to be created without having to be configured as all calls will pass up to this parent logger.

    :param log_level: (Optional) - allows the default setlevel to be overridden.
    :return: parent logger instance
    """

    # Create logger
    api_logger = logging.getLogger('uscc_eng_parser_api')
    api_logger.setLevel(log_level)
    # Create file handler
    fh = logging.FileHandler('uscc_eng_parser_api.log', mode='w')
    fh.setLevel(log_level)
    # Create console stream handler.
    # ch = logging.StreamHandler()
    # ch.setLevel(log_level)
    # Create message formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s:%(module)s - %(levelname)s - %(message)s',
                                  datefmt='%m/%d/%Y - %I:%M:%S %p')
    fh.setFormatter(formatter)
    # ch.setFormatter(formatter)
    # Add the handlers to the logger
    api_logger.addHandler(fh)
    # api_logger.addHandler(ch)
    return api_logger


if __name__ == '__main__':
    main()
