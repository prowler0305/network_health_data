from hbase_resources.Base_HBASE import *
from common.common import Common


class HbaseTableAction(BaseHbase):
    """
    Class that encapsulates building the HBASE URL that can be performed on a table. E.g. schema, regions, etc.
    """
    def __init__(self, request_keyword, api_args):
        BaseHbase.__init__(self, request_keyword, api_args)
        self.action = None

    def build_request(self):
        """

        :return:
        """

        expected_parms = ['action_type']
        super_rc, bad_parm = super().build_parameters()
        # TODO: If going with WNG Version 2 then don't need to check return code if 'table_name' not present.
        # add_argument method handles this (required=True)
        if not super_rc:
            error_text = "'%s' parameter is required and was either not found or found to not have a value. Please include" \
                         " parameter with request and try again." % bad_parm
            return Common.generate_error_response(self.error_msg_key, error_text, 400)

        for parm in expected_parms:
            rc, value = self.get_parm_value(parm)
            if rc:
                if parm == 'action_type':
                    self.action = value.lower()
                else:
                    continue
            else:
                error_text = "Parameter 'hbase_keyword' value of %s requires the '%s' parameter to be provided. " \
                             "Please include parameter with request and retry." % (self.request, parm)
                return Common.generate_error_response(self.error_msg_key, error_text, 400)

        return True

    def execute_request(self):
        """

        :return:
        """

        if self.action == 'schema' or self.action == 'regions':
            return self.get_url()
        else:
            not_implemented_message = "WNG API action '%s' is not available. Please see WNG API documentation." % self.action
            response = Common.generate_error_response(self.error_msg_key, not_implemented_message, 501)

        return response

    def get_url(self):
        """
        Returns the HBASE URL needed to get a list of all the tables.

        :return: sets self.hbase_url class instance variable.
        """

        self.url = self.get_base_url()
        self.url = self.url + self.table_name + '/' + self.action
        response = super().format_hbase_url_response()
        return response
