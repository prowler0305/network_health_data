import cx_Oracle
import logging


class QueryOracle(object):
    """
    Encapsulate interactions with an Oracle DB.

    """
    def __init__(self, username, password, oracle_host_name, port_num, service_dbname, logger_name):
        """

        :param username:
        :param password:
        :param oracle_host_name:
        :param port_num:
        :param service_dbname:
        :return:
        """

        self.username = username
        self.password = password
        self.host_name = oracle_host_name
        self.port_num = port_num
        self.dbname = service_dbname

        self.connect_string = "{}/{}@{}:{}/{}".format(self.username, self.password, self.host_name, self.port_num,
                                                      self.dbname)
        self.oracle_connection = None
        self.logger_name = logger_name
        self.nh_logger = logging.getLogger(self.logger_name)


    def establish_connect(self):
        """
        Establishes the connect to the Oracle DB using the self.connection_string class attribute.

        If a successful connection is made the class attribute 'self.oracle_connection' is updated

        :return: True/False
        """

        if self.connect_string is not None:
            self.oracle_connection = cx_Oracle.connect(self.connect_string)
        else:
            self.nh_logger.error("Connection to Oracle database '{}' can't be establshed, oracle connection string '{}' "
                                 "invalid".format(self.dbname, self.connect_string))
