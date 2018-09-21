import os
from common.common import Common
import logging.config


class NhBase(object):
    """

    """
    def __init__(self):
        self.logger_name = 'network_health_data'
        self.nh_logger = None

    def establish_logging(self, logger_config_json=None):
        """
        Establishes a logger instance.
        :param logger_config_json: Path to a JSON configuration file
        :return:
        """

        if logger_config_json is not None:
            rc, logger_config_dict = Common.read_json_file(logger_config_json)
            if rc:
                logging.config.dictConfig(logger_config_dict)
                self.nh_logger = logging.getLogger(self.logger_name)
        else:
            numerical_level = getattr(logging, os.environ.get('log_level').upper(), None)
            if not isinstance(numerical_level, int):
                raise ValueError("Invalid log level: {}".format(os.environ.get('log_level')))
            logging.basicConfig(level=numerical_level)
            self.nh_logger = logging.getLogger(self.logger_name)
