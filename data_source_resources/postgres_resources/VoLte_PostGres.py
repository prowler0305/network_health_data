from common.common import Common
from flask import jsonify
from data_source_resources.postgres_resources.Base_PostGres import *
from core.RequestParms import RequestParms


class VolteInvestigation(BasePostGres):
    """
    Base parent class in which other specific PostGres classes can inherit from. This class can and will contain either
    generic methods or methods which are overloaded by specific subclasses.
    """

    def __init__(self, request_keyword, api_args):
        BasePostGres.__init__(self, request_keyword, api_args, host=api_args.get('host'),
                              database=api_args.get('database'), port=api_args.get('port'), user=api_args.get('user'),
                              password=api_args.get('password')
                              )
        self.sql_cmd = None
        self.sql_params = None
        self.msg_key = 'volte_investigation'

    def build_request(self):
        """

        :return:
        """

        expected_parms = ['sql_cmd']
        optional_parms = ['sql_params']

        for parm in expected_parms:
            rc, value = self.get_parm_value(parm)
            if rc:
                if parm == 'sql_cmd':
                    self.sql_cmd = value
            else:
                error_text = "Parameter '%s' needs to be provided in order to execute SQL against a database. Please " \
                             "include it in the POST body." % parm
                return False, Common.generate_error_response(self.msg_key, error_text, 400)

        for parm in optional_parms:
            rc, value = self.get_parm_value(parm)
            if rc:
                if parm == 'sql_params':
                    self.sql_params = value
            else:
                continue

        return True, ""

    def execute_request(self):
        """

        :return:
        """

        volte_response = None
        if self.establish_connection():
            if self.create_cursor():
                if self.execute_statement(self.sql_cmd, self.sql_params):
                    if self.commit_work():
                        volte_response = jsonify({self.msg_key: 'successful'})
                        volte_response.status_code = 200
                else:
                    volte_response = jsonify({self.msg_key: self.pg_exception.pgerror})
                    volte_response.status_code = 422
        else:
            volte_response = Common.generate_error_response('volte_message', 'unsuccessful', 500)

        return volte_response
