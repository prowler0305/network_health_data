import psycopg2


class BasePostGres(object):
    """
    Base parent class in which other specific PostGres classes can inherit from. This class can and will contain either
    generic methods or methods which are overloaded by specific subclasses.
    """

    def __init__(self, host, database, port, user, password):
        """

        :param host:
        :param database:
        :param port:
        :param user:
        :param password:
        """

        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.password = password
        self.connection_info = dict()
        self._pg_connection = None
        self._pg_cursor = None
        for attr in self.__dict__.keys():
            if attr != 'connection_info':
                self.connection_info[attr] = self.__dict__.get(attr)

    def establish_connection(self):
        """
        Establish a connection to PostGres database using the connection information stored in the connection_info
        class instance variable

        :return: True if a connection was not already established. False if self.connection is already set.
        """

        if self._pg_connection is not None:
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
        :return:
        """

        if self._pg_cursor is not None:
            self._pg_cursor.execute(sql_cmd, sql_params)
            return True

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
