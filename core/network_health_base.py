import os
from common.common import Common
import logging
import logging.config


class NhBase(object):
    """

    """
    def __init__(self):


        self.environ_vars_config_path = os.environ.get('env_vars_config')
        self.logger_name = 'network_health_data'
        self.nh_logger = None
        self.svt_test_sql = """SELECT c_alarmsource, c_lastoccurrence, c_summary, c_alertkey, c_suppressescl, c_ttnumber
         FROM netcoold.alerts_status_t WHERE c_lastoccurrence > (SYSTIMESTAMP - .0833)
          AND c_alertgroup = 'ASCOM Availibility Alarms' ORDER BY 1,4,2 """

        self._get_environment_vars()

    def _get_environment_vars(self):
        """
        If the OS level environment variables 'env_vars_config' exists, then reads the json
        config file and converts it to a dictionary. Then loops through the keys in the config
        dictionary and for every key sets a class instance attribute using the key and its
        related value. A key can exists but doesn't have to contain a value(i.e. "key": "" or
        "key": null), in both cases then the value for the attribute will be set to None.

        :return: Nothing. class instance attributes are created.
        """
        if self.environ_vars_config_path is None:
            raise RuntimeError("Environment variable config file is not present, environment variable 'env_vars_config' "
                               "is missing.")
        else:
            env_config_rc, env_config_dict = Common.read_json_file(self.environ_vars_config_path)
            if not env_config_rc:
                raise RuntimeError("Environment variable config dictionary could not be obtained."
                                   " Path to file specified: {}".format(self.environ_vars_config_path))
            else:
                for env_var_key, env_var_value in env_config_dict.items():
                    if env_var_value is None or env_var_value == "":
                        setattr(self, env_var_key, None)
                    else:
                        setattr(self, env_var_key, env_var_value)

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
