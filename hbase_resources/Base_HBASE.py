from flask import jsonify
from core.RequestParms import RequestParms


class BaseHbase(object):
    """
    Base parent class in which other specific Hbase classes can inherit from. This class can and will contain either
    generic methods or methods which are overloaded by specific test class methods.
    """

    def __init__(self, request_keyword, api_args):
        self.request = request_keyword
        self.request_args = api_args
        self.hbase_root_url = "http://ilscha03-hden-01.uscc.com:20550/"
        self.error_msg_key = "wng_api_msg"
        self.url = None
        self.table_name = None
        self.common_expected_parms_list = ['table_name']

    def service_request(self):
        """
        Base method that can be overridden in subclasses
        :return:
        """
        return

    def get_base_url(self):
        """
        Base method that can be overridden in subclasses
        :return:
        """
        return self.hbase_root_url

    def build_parameters(self):
        """
        Check and set all the expected and optional parameters that are needed for any WNG API request.
        :return:
        """

        for parm in self.common_expected_parms_list:
            rc, value = self.get_parm_value(parm)
            if rc:
                if parm == 'table_name':
                    self.table_name = value.lower()
                else:
                    continue
            else:
                return False, parm
        return True, ""

    def get_parm_value(self, parameter_to_find):
        """
        Tried to find the value for the parameter requested for in the request arguments dictionary.
        :param parameter_to_find:
        :return: Tuple returned by check_parms in py:class RequestParms
        """

        return RequestParms.check_parms(self.request_args, parameter_to_find)

    def generate_error_response(self, error_text, response_code):
        """
        Formats a simple error message to be returned in http response as a JSON object.
        :param error_text: Message text to be returned. It will be sent as a part of a JSON response with the
        "wng_api_msg" key value. (i.e. {"msg_api_msg": "<error_text>"})
        :param response_code: the HTTP response code to be set as the response.status_code
        :return: Error message and status code in a JSON format
        """

        error_response = jsonify({self.error_msg_key: error_text})
        error_response.status_code = response_code
        return error_response

    def format_hbase_url_response(self, sending_url=None, status_code_override=200):
        """
        Formats the sending of the HBASE URL creating by the URL service class and the status code into a JSON response.

        :param sending_url: (Optional) - Can override the url to be sent back, otherwise defaults to use the class "url"
            variable.
        :param status_code_override: Overrides the default status code of '200'.
        :return: HBASE url and status code in a JSON format.
        """

        if sending_url is None:
            url_response = jsonify({'hbase_url': self.url})
        else:
            url_response = jsonify({'hbase_url': sending_url})

        url_response.status_code = status_code_override
        return url_response
