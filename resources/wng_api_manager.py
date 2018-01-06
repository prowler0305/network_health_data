from flask import jsonify
from flask_restful import Resource, reqparse
from core.Builder import HbaseBuilder
from common.common import Common


class WngApiManager(Resource):
    """~
    """
    @staticmethod
    def get():
        """
        Main landing URL for the WNG API manager.

        Test with cURL command:
            curl "http://localhost:5000/wng_api?hbase_keyword=view1"

        :param: hbase_keyword: Indicates what HBASE data view the users wants. This keyword resolves to a HBASE URL.
        :return: HBASE URL
        """

        list_o_hbase_requests = ['table', 'list_all', 'action']
        list_o_actions = ['schema', 'regions']
        error_key_str = 'wng_api_msg'

        # Establish request parser and add arguments
        hbase_keyword_help_message = "Parameter 'hbase_keyword' either missing or incorrect value given. Choices are [%s]." % list_o_hbase_requests
        action_keyword_help_message = "Parameter 'action' either missing or incorrect value given. Choices are [%s]." % list_o_actions
        wng_parser = reqparse.RequestParser()
        wng_parser.add_argument('hbase_keyword', required=True, choices=list_o_hbase_requests, help=hbase_keyword_help_message)
        wng_parser.add_argument('action', choices=list_o_actions, help=action_keyword_help_message)
        wng_parser.add_argument('table_name', store_missing=False)

        args = wng_parser.parse_args(strict=True)
        service_instance = HbaseBuilder.build_hbase_service(args.get('hbase_keyword'), args)
        if service_instance is not None:
            response = service_instance.service_request()
        else:
            error_text = "hbase_keyword parameter is a valid value but has not been implemented. " \
                         "Please contact Automation team."
            response = Common.generate_error_response(error_key_str, error_text, 500)
        return response


