from hbase_resources.hbase_list_tables import HbaseListTables
from hbase_resources.hbase_table_actions import HbaseTableAction


class DBbuilder(object):
    """
    Static class that contains static methods to service different WNG API Endpoints
    """

    db_service_dict = {'hbase_list_all': HbaseListTables, 'hbase_action': HbaseTableAction}

    @staticmethod
    def build_service(db_service, request_args):
        """
        Creates and returns the correct class instance needed based on the database service request.

        :param db_service: Database Service class request keyword. (e.g. 'hbase_list_all')
        :param request_args: Dictionary of arguments from HTTP request.
        :return: instance of correct hbase class
        """

        if db_service in DBbuilder.db_service_dict:
            service_instance = DBbuilder.db_service_dict.get(db_service)(db_service, request_args)
            return service_instance
