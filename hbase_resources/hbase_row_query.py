from hbase_resources.Base_HBASE import *
from common.common import Common


class HbaseRowQuery(BaseHbase):
    """
    Class that encapsulates building the HBASE URL to query data for a single row in HBASE
    """
    def __init__(self, request_keyword, api_args):
        BaseHbase.__init__(self, request_keyword, api_args)
        self.rownum = None

    def build_request(self):
        """

        :return:
        """

        expected_parms = ['row_number']
        super_rc, bad_parm = super().build_parameters()
        if not super_rc:
            error_text = "'%s' parameter is required and was either not found or found to not have a value. Please include" \
                         " parameter with request and try again." % bad_parm
            return False, Common.generate_error_response(self.error_msg_key, error_text, 400)

        for parm in expected_parms:
            rc, value = self.get_parm_value(parm)
            if rc:
                if parm == 'row_number':
                    self.rownum = value
                else:
                    continue
            else:
                error_text = "Parameter 'hbase_keyword' value of %s requires the '%s' parameter to be provided. " \
                             "Please include parameter with request and retry." % (self.request, parm)
                return False, Common.generate_error_response(self.error_msg_key, error_text, 400)

        return True, ""

    def execute_request(self):
        """

        :return:
        """

        if self.rownum is not None:
            return self.get_url()
        else:
            not_implemented_message = "USCC Engineering API API row number is not valid. Please see USCC Engineering API API documentation."
            response = Common.generate_error_response(self.error_msg_key, not_implemented_message, 501)

        return response

    def get_url(self):
        """
        Returns the HBASE URL needed to get a list of all the tables.

        :return: sets self.hbase_url class instance variable.
        """

        self.url = self.get_base_url()
        self.url = self.url + self.table_name + '/' + self.rownum
        response = super().format_hbase_url_response()
        return response
