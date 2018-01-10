from flask import jsonify
from flask_restful import Resource
from core.Builder import DBbuilder
from common.common import Common


class ListAll(Resource):
    """~
    """
    @staticmethod
    def get():
        """
        Services requests to get a list of all of the tables in the database requested. Ending action is different
        based on the database requested. See documentation below for reference.

        ---------------------------------------------------------------------------------------------------------------
        |Database | Returned Information                                                                              |
        ---------------------------------------------------------------------------------------------------------------
        | HBASE   | REST API URL needed to get the list of tables                                                     |
        ---------------------------------------------------------------------------------------------------------------
        | DB Name | information on returned data (duplicate this line first before adding new entry)                  |
        ---------------------------------------------------------------------------------------------------------------

        :return: standard HTTP response
        """
        common_service_request = 'list_all'

        uscc_eng_parser = Common.create_api_parser()
        Common.add_common_request_args(uscc_eng_parser)
        args = Common.parse_request_args(uscc_eng_parser)
        database_service_request_key = args.get('db_name') + '_' + common_service_request
        service_instance = DBbuilder.build_service(database_service_request_key, args)
        if service_instance is not None:
            build_rc = service_instance.build_request()
            if build_rc:
                response = service_instance.execute_request()
                return response
            else:
                return build_rc
        # TODO: what HTTP error status should we return here. Maybe 501?
