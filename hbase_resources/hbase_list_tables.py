from hbase_resources.Base_HBASE import *


class HbaseListTables(BaseHbase):
    """
    Class that encapsulates listing all the tables in HBASE.
    """
    def __init__(self, request_keyword, api_args):
        BaseHbase.__init__(self, request_keyword, api_args)

    def build_request(self):
        """
        Build service request for listing all tables in HBASE. No additional parameters needed to service request beyond
        what was done by RequestParser.

        :return: Just return to caller.
        """
        return True, ""

    def execute_request(self):
        """

        :return:
        """

        response = jsonify({'hbase_url': self.get_base_url()})
        response.status_code = 200

        return response
