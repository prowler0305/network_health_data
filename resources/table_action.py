from flask import jsonify
from flask_restful import Resource
from core.Builder import DBbuilder
from common.common import Common


class TableAction(Resource):
    """~
    """
    @staticmethod
    def get():
        """
        Services requests to perform a table level action. Ending action is different based on the database requested.
        See documentation below for reference.

        ---------------------------------------------------------------------------------------------------------------
        |Database | Returned Information                                                                              |
        ---------------------------------------------------------------------------------------------------------------
        | HBASE   | REST API URL needed to get the list of tables                                                     |
        ---------------------------------------------------------------------------------------------------------------
        | DB Name | information on returned data (duplicate this line first before adding new entry)                  |
        ---------------------------------------------------------------------------------------------------------------

        :return: standard HTTP response
        """
        common_service_request = 'action'
        list_o_actions = ['schema', 'regions']
        action_keyword_help_message = "Value given is not a valid choice. Choices are %s. " \
                                      % list_o_actions

        wng_parser = Common.create_api_parser()
        Common.add_common_request_args(wng_parser)
        wng_parser.add_argument('action_type', choices=list_o_actions, default='schema', help=action_keyword_help_message)
        wng_parser.add_argument('table_name', required=True)
        args = Common.parse_request_args(wng_parser)
        database_service_request_key = args.get('db_name') + '_' + common_service_request
        service_instance = DBbuilder.build_service(database_service_request_key, args)
        if service_instance is not None:
            build_rc = service_instance.build_request()
            if build_rc:
                response = service_instance.execute_request()
            else:
                response = build_rc

        return response
