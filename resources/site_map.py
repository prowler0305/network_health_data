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

        endpoint_dict = {}
        uscc_eng_app = flask.current_app
        for rule in uscc_eng_app.url_map.iter_rules():
            url = rule.rule
            if 'row_query' in url:
                endpoint_dict[url] = 'Query the database name requesting for a single row of data'
            elif 'list_all' in url:
                endpoint_dict[url] = 'List all the tables in the database name requested'
            elif 'action' in url:
                endpoint_dict[url] = 'Query information about a specific table in the database requests. (E.g. schema)'
            else:
                continue

        response = jsonify(endpoint_dict)
        response.status_code = 200
        return response
