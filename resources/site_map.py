import flask
from flask import jsonify
from flask_restful import Resource


class SiteMap(Resource):
    """~
    """
    @staticmethod
    def get():
        """
        Services request to the base host url which calls the SiteMap class to return the list of site routes.

        :return: standard HTTP response
        """

        endpoint_dict = dict(row_query='Query the database name requesting for a single row of data',
                             list_all='List all the tables in the database name requested',
                             action='Query information about a specific table in the database requests. (E.g. schema)'
                             )

        endpoint_url_dict = {}
        uscc_eng_app = flask.current_app
        for rule in uscc_eng_app.url_map.iter_rules():
            url = rule.rule
            for endpoint_key, endpoint_description in endpoint_dict.items():
                if endpoint_key in url:
                    endpoint_url_dict[url] = endpoint_description

        response = jsonify(endpoint_dict)
        response.status_code = 200
        return response
