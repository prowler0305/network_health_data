import flask
from flask import jsonify
from flask_restful import Resource, fields, marshal


api_urls = {
    'uri1': fields.Url('sitemap', absolute=True),
    'uri2': fields.Url('listall', absolute=True),
    'uri3': fields.Url('tableaction', absolute=True),
    'uri4': fields.Url('rowquery', absolute=True),
    'uri5': fields.Url('scanning', absolute=True),
    'uri6': fields.Url('imsi', absolute=True)
}


class SiteMap(Resource):
    """~
    """
    @staticmethod
    def get():
        """
        Services request to the base host url which calls the SiteMap class to return the list of site routes.

        :return: standard HTTP response
        """

        endpoint_description_dict = dict(row_query='Query the database name requesting for a single row of data',
                                         list_all='List all the tables in the database name requested',
                                         action='Query information about a specific table in the database requests. (E.g. schema)',
                                         imsis='Interacts with the imis tracking file',
                                         scan='Creates a Scanner object for use with Hbase'
                                         )

        # endpoint_url_dict = {}
        # uscc_eng_app = flask.current_app
        # for rule in uscc_eng_app.url_map.iter_rules():
        #     url = rule.rule
        #     for endpoint_key, endpoint_description in endpoint_dict.items():
        #         if endpoint_key in url:
        #             endpoint_url_dict[url] = endpoint_description

        temp_dict = {}
        marshal_dict = marshal(api_urls, api_urls)
        for url_key in api_urls.keys():
            for descrip_key in endpoint_description_dict.keys():
                if descrip_key in marshal_dict.get(url_key):
                    temp_dict[marshal_dict.get(url_key)] = endpoint_description_dict.get(descrip_key)

        response = jsonify(temp_dict)
        response.status_code = 200
        return response
