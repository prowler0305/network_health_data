from flask import jsonify
from flask_restful import Resource
from core.Builder import DBbuilder
from common.common import Common


class Scanning(Resource):
    """~
    """
    @staticmethod
    def put():
        """
        Services requests to perform a table level action. Ending action is different based on the database requested.
        See documentation below for reference.

        ---------------------------------------------------------------------------------------------------------------
        |Database | Returned Information                                                                              |
        ---------------------------------------------------------------------------------------------------------------
        | HBASE   | REST API URL needed to do a multirow fetch operation                                              |
        ---------------------------------------------------------------------------------------------------------------
        | DB Name | information on returned data (duplicate this line first before adding new entry)                  |
        ---------------------------------------------------------------------------------------------------------------

         curl -i --negotiate -u: -H "Accept: application/json" -H "Content-Type: text/xml" -d '<Scanner batch="1"/>' -X PUT "http://ilscha03-hden-01.uscc.com:20550/enodeb/scanner"

        :return: standard HTTP response
        """
        common_service_request = 'scan'
        # action_keyword_help_message = "Value given is not a valid choice. Choices are %s. " \
        #                               % list_o_actions

        uscc_eng_parser = Common.create_api_parser()
        Common.add_common_request_args(uscc_eng_parser)
        uscc_eng_parser.add_argument('table_name', required=True)
        uscc_eng_parser.add_argument('scan_filter_data', required=True)
        args = Common.parse_request_args(uscc_eng_parser)
        database_service_request_key = args.get('db_name') + '_' + common_service_request
        service_instance = DBbuilder.build_service(database_service_request_key, args)
        if service_instance is not None:
            build_rc = service_instance.build_request()
            if build_rc:
                response = service_instance.execute_request()
            else:
                response = build_rc

        return response
