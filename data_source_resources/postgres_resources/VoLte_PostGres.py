from common.common import Common
from flask import jsonify
from data_source_resources.postgres_resources.Base_PostGres import *


class VolteInvestigation(BasePostGres):
    """
    Base parent class in which other specific PostGres classes can inherit from. This class can and will contain either
    generic methods or methods which are overloaded by specific subclasses.
    """

    def __init__(self, request_keyword, api_args, sql_cmd, sql_params):
        BasePostGres.__init__(self, host=api_args.get('host'), database=api_args.get('database'),
                              port=api_args.get('port'), user=api_args.get('user'), password=api_args.get('password'))
        self.request = request_keyword
        self.sql_cmd = sql_cmd
        self.sql_params = sql_params

    def build_request(self):
        """

        :return:
        """

        return True

    def execute_request(self):
        """

        :return:
        """

        volte_response = None
        if self.establish_connection():
            if self.create_cursor():
                if self.execute_statement(self.sql_cmd, self.sql_params):
                    volte_response = jsonify({'volte_db_load': 'successful'})
                    volte_response.status_code = 200
        else:
            volte_response = Common.generate_error_response('volte_message', 'unsuccessful', 500)

        return volte_response
