from flask import jsonify
from flask_restful import Resource
from common.common import Common


class FUT(Resource):
    """~
    """
    @staticmethod
    def get():
        """

        :return: standard HTTP response
        """

        list_o_subscriber_ids = []
        dict_of_subscribers = {}
        fut_subscribers_file = '/home/aspea002/IdeaProjects/USCC_ENG_API/data_only/FUT-subscribers'
        with open(fut_subscribers_file) as fut_fh:
            for line in fut_fh:
                line = line.rstrip('\n')
                list_o_subscriber_ids.append(line)

        for subscriber_id in list_o_subscriber_ids:
            print(subscriber_id)

        for list_index in range(len(list_o_subscriber_ids)):
            dict_of_subscribers[list_index] = list_o_subscriber_ids[list_index]

        response = jsonify(dict_of_subscribers)
        response.status_code = 200
        return response
