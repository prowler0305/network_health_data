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
        self.logger_name = logger_name
        self.nh_logger = logging.getLogger(self.logger_name)

        self.dsn = "{}:{}/{}".format(self.host_name, self.port_num, self.dbname) if all([self.host_name, self.port_num, self.dbname]) else None
        self.oracle_connection = None
        self.oracle_cursor = None

    def establish_connect(self) -> bool:
        """
        Establishes the connect to the Oracle DB using the self.connection_string class attribute.

        If a successful connection is made the class attribute 'self.oracle_connection' is updated

        :return: True/False
        """

        connection_error_msg = "Connection to Oracle database '{}' can't be establshed. Oracle connection info User "\
                               "name: '{}', Password: '{}', Host: '{}', Port: '{}'".format(self.dbname, self.username,
                                                                                           self.password,
                                                                                           self.host_name,
                                                                                           self.port_num)
        if self.dsn is not None:
            try:
                # self.oracle_connection = cx_Oracle.connect("automation_ro/automation_ro@shracdev-scan.uscc.com:1521/netcoold")
                self.oracle_connection = cx_Oracle.connect(self.username, self.password, self.dsn)
                return True
            except Exception as oracle_excp:
                self.nh_logger.exception(connection_error_msg)
                return False
        else:
            self.nh_logger.error(connection_error_msg)
            return False

    def create_cursor(self) -> bool:
        """
        Creates the oracle cursor object. Requires that the establish_connect() method has been called first. Sets the
        class attribute: self.oracle_cursor

        :return: True/False
        """

        if self.oracle_connection is not None:
            try:
                self.oracle_cursor = self.oracle_connection.cursor()
                return True
            except cx_Oracle.DatabaseError as oracle_cursor_error:
                self.nh_logger.exception("Can not create oracle cursor")
                return False
        else:
            self.nh_logger.error("Connection to oracle database has not be established. The method "
                                 "establish_connection() needs to be called first.")
            return False

    def execute_sql(self, sql_string: str) -> bool:
        """
        Given a string that contains an SQL statement, uses the self.oracle_cursor to execute the statement.

        :param sql_string: An SQL statement passed as a string.
        :return: True - The statement was executed without any issues.
                False - The statement did not execute successfully. Error message are available in the 'errors object'
        """

        if self.oracle_cursor is None and self.oracle_connection is not None:
            if not self.create_cursor():
                return False

        if self.oracle_cursor is not None:
            try:
                self.oracle_cursor.execute(sql_string)
                return True
            except cx_Oracle.DatabaseError as oracle_exec_error:
                self.nh_logger.exception("Error executing SQL: {}".format(sql_string))
                return False
        else:
            return False

    def retrieve_results(self, retrieve_type: str='all', return_as_dict: bool=True) -> List[dict]:
        """
        Fetches the results from an SQL query. Can either fetch either all rows at once or one at time. Can return the
        results as a list of dictionary object that joins the column names and the data together as key: value pairs.
        This allows you to iterate over each row in the results set and access the data using dictionary object attributes
        and methods. If you turn off this setting then the data is returned as the original data object created by the
        cx_Oracle package. See the :return section below for details.

        If this method is called before the :class QueryOracle: execute_sql() method an exception is raised by the
        cx_Oracle package which is caught and logged in which 'False' is returned.

        Additionally if any parameters are passed with invalid values then an error message is logged and 'False' is
        returned.


        :param retrieve_type: Choices are 'all' or a positive integer indicating the number of rows to fetch.
                                Defaults to 'all'.
        :param return_as_dict: Build a dictionary of the results and the tables columns into a Python dictionary object
                                to be returned.
        :return: False if parameters are invalid otherwise the result set in one of the below ways depending on the
                    param: retrieve_type above:
                        1. As the requested dictionary.
                            a. If no more rows are available an empty dictionary is returned.
                        2. The original data structure depending on whether fetching one, many, or all rows was requested.
                            a. If fetching many or all then a list of tuples is returned
                                i. If no more rows available then an empty list is returned.
                            b. If fetching one row then a single tuple.
                                i. None is returned if no more data is available.
        """

        fetch_num_rows = None
        if retrieve_type != 'all' and not retrieve_type.isnumeric():
            self.nh_logger.error("Parameter retrieve_type is not valid, choices are 'all' or an integer >= 1. Got value of {} instead.".format(retrieve_type))
            return False
        elif retrieve_type.isnumeric():
            if not int(retrieve_type) >= 1:
                self.nh_logger.error("Parameter retrieve_type is not >= 1. Value given was '{}'".format(retrieve_type))
                return False
            else:
                fetch_num_rows = int(retrieve_type)
        else:
            pass

        if return_as_dict:
            # Gets all the column names for the result set
            column_name_list = [x[0] for x in self.oracle_cursor.description]

        try:
            if fetch_num_rows is None:
                if return_as_dict:
                    return [dict(zip(column_name_list, row)) for row in self.oracle_cursor.fetchall()]
                else:
                    return self.oracle_cursor.fetchall()
            elif fetch_num_rows == 1:
                if return_as_dict:
                    return [dict(zip(column_name_list, self.oracle_cursor.fetchone()))]
                else:
                    return(self.oracle_cursor.fetchone())
            else:
                if return_as_dict:
                    return [dict(zip(column_name_list, row)) for row in self.oracle_cursor.fetchmany(numRows=fetch_num_rows)]
                else:
                    return self.oracle_cursor.fetchmany(numRows=fetch_num_rows)
        except cx_Oracle.DatabaseError:
            self.nh_logger.exception("Call to :class QueryOracle: execute_sql() must be called before the "
                                     "retrieve_results() method can be called")
            return False