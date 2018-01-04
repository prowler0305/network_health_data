from hbase_resources.Base_HBASE import *


class ListTables(BaseHbase):
    """
    Class that encapsulates producing the different URL(s) to interact with HBASE.
    """
    def __init__(self, request_keyword):
        BaseHbase.__init__(self, request_keyword)

    def service_request(self):
        """

        :return:
        """

        if self.request == 'list_all':
            if self.get_url():
                response = jsonify({'url': self.hbase_url})
                response.status_code = 200
            else:
                response = jsonify({self.hbase_msg_key: "Error retrieving URL for 'list_all' request."})
                response.status_code = 500
        else:
            not_implemented_message = "WNG API request '%s' is not implemented." % self.request
            response = jsonify({self.hbase_msg_key: not_implemented_message})
            response.status_code = 501

        return response

    def get_url(self):
        """
        Returns the HBASE URL needed to get a list of all the table regions

        :return: sets self.hbase_url class instance variable.
        """

        self.hbase_url = BaseHbase.hbase_rool_url
        return True
