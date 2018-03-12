from flask_restful import Resource
from core.Builder import DBbuilder
from common.common import Common


class VolteLoad(Resource):
    """
    """
    @staticmethod
    def post():
        """
        Services a requests to load data into a PostGres database for use with the Volte Investigation Kafka Consumer
        Clients.

        :return: standard HTTP response
        """

        uscc_eng_parser = Common.create_api_parser()
        uscc_eng_parser.add_argument('host', required=True)
        uscc_eng_parser.add_argument('database', required=True)
        uscc_eng_parser.add_argument('port', required=True)
        uscc_eng_parser.add_argument('user', required=True)
        uscc_eng_parser.add_argument('password', required=True)
        uscc_eng_parser.add_argument('sql_cmd', required=True)
        uscc_eng_parser.add_argument('sql_params')
        args = Common.parse_request_args(uscc_eng_parser)
        database_service_request_key = 'volte_kcc'
        service_instance = DBbuilder.build_service(database_service_request_key, args)
        if service_instance is not None:
            build_rc, build_response = service_instance.build_request()
            if build_rc:
                response = service_instance.execute_request()
            else:
                response = build_response

        return response
