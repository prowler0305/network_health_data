from hbase_resources.hbase_list_tables import ListTables


class HbaseBuilder(object):
    """
    Static class that contains static methods to service building an HBASE URL requests.
    """

    hbase_class_dict = {'list_all': ListTables}

    @staticmethod
    def build_hbase_service(request_service):
        """
        Creates and returns the correct class instance needed based on the hbase_keyword.

        :param request_service: Hbase service request keyword. (e.g. 'list_all')
        :return: instance of correct hbase class
        """

        if request_service in HbaseBuilder.hbase_class_dict:
            service_instance = HbaseBuilder.hbase_class_dict.get(request_service)(request_service)
            return service_instance
