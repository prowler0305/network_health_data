import psycopg2
from core.RequestParms import RequestParms
from common.common import Common


class BasePostGres(object):
    """
    Base parent class in which other specific PostGres classes can inherit from. This class can and will contain either
    generic methods or methods which are overloaded by specific subclasses.
    """

    def __init__(self, request_keyword, api_args, host, database, port, user, password):
        """

        :param request_keyword:
        :param api_args:
        :param host:
        :param database:
        :param port:
        :param user:
        :param password:
        """

        self.request = request_keyword
        self.request_args = api_args
        self._pg_connection = None
        self._pg_cursor = None
        self.msg_key = 'uscc_postgres_api'
        self.pg_exception = None

        # Warning: These attributes must stay grouped together and connection_info must be defined last
        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.password = password
        self.connection_info = dict(host=self.host,
                                    database=self.database,
                                    port=self.port,
                                    user=self.user,
                                    password=self.password
                                    )
        # Warning: End -------------------------------------------------------------------------------------------------
        # for attr in self.__dict__.keys():
        #     if attr != 'connection_info':
        #         self.connection_info[attr] = self.__dict__.get(attr)

    def get_parm_value(self, parameter_to_find):
        """
        Try to find the value for the parameter requested for in the request arguments dictionary.
        :param parameter_to_find:
        :return: Tuple returned by check_parms in py:class RequestParms
        """

        return RequestParms.check_parms(self.request_args, parameter_to_find)

    def establish_connection(self):
        """
    Establish a connection to PostGres database using the connection information stored in the connection_info
    class instance variable

    :return: True if a connection was not already established. False if self.connection is already set.
    """

        if self._pg_connection is None:
            self._pg_connection = psycopg2.connect(**self.connection_info)
            return True

        return False

    def create_cursor(self):
        """
        Using the database connection, creates a cursor object.

        :return: True if a cursor object could be created and set, False if the connection object doesn't exist.
        """

        if self._pg_connection is not None:
            self._pg_cursor = self._pg_connection.cursor()
            return True

        return False

    def execute_statement(self, sql_cmd, sql_params):
        """

        :param sql_cmd:
        :param sql_params:
        :return: True or False - any errors during command execution are contain in the class attribute.
        """

        if self._pg_cursor is not None:
            try:
                self._pg_cursor.execute(sql_cmd, sql_params)
                return True
            except psycopg2.Error as pg_e:
                self.pg_exception = pg_e
                return False

        return False

    def commit_work(self):
        """

        :return:
        """

        if self._pg_connection is not None:
            self._pg_connection.commit()
            return True

        return False

    def close_connection(self):
        """

        :return:
        """

        if self._pg_connection is not None:
            if self._pg_cursor is not None:
                self._pg_cursor.close()

            self._pg_connection.close()
            return True

        return False
