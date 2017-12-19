import argparse
import logging
import log_tutorial


def main():
    """

    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--log')
    args = vars(parser.parse_args())
    if args.get('log') is not None:
        log_level = args.get('log')
    else:
        log_level = 'INFO'

    numerical_log_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numerical_log_level, int):
        raise ValueError('Invalid log level: %s. Valid values are: %s' % (log_level,
                                                                          'DEBUG, INFO, WARNING, ERROR, or CRITICAL'))
    logging.basicConfig(filename='example.log', filemode='w', level=numerical_log_level,
                        format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    print(logging.getLogger().getEffectiveLevel())
    print(logging.getLevelName(numerical_log_level))
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    logging.warning('And this too')
    log_tutorial.logging_tutorial()


if __name__ == '__main__':
    main()
