from hbase_resources.Base_HBASE import *


class ListTables(BaseHbase):
    """
    Class that encapsulates listing all the tables in HBASE.
    """
    def __init__(self, request_keyword, api_args):
        BaseHbase.__init__(self, request_keyword, api_args)

    def service_request(self):
        """

        :return:
        """

        response = jsonify({'hbase_url': self.get_base_url()})
        response.status_code = 200

        return response
