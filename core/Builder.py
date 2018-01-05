from hbase_resources.hbase_list_tables import ListTables
from hbase_resources.hbase_table_actions import TableAction


class HbaseBuilder(object):
    """
    Static class that contains static methods to service building an HBASE URL requests.
    """

    hbase_class_dict = {'list_all': ListTables, 'action': TableAction}

    @staticmethod
    def build_hbase_service(request_service, request_args):
        """
        Creates and returns the correct class instance needed based on the hbase_keyword.

        :param request_service: Hbase service request keyword. (e.g. 'list_all')
        :param request_args: Dictionary of arguments from HTTP request.
        :return: instance of correct hbase class
        """

        if request_service in HbaseBuilder.hbase_class_dict:
            service_instance = HbaseBuilder.hbase_class_dict.get(request_service)(request_service, request_args)
            return service_instance
