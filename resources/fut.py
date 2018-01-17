import sys
from flask import jsonify
from flask_restful import Resource
from common.common import Common


class FUT(Resource):
    """
    """
    if sys.argv[1] != '--dev':
        fut_subscribers_file = '/opt/app-root/src/data_only/FUT-Subscribers'
    else:
        fut_subscribers_file = '/home/aspea002/IdeaProjects/USCC_ENG_API/data_only/FUT-subscribers'

    @staticmethod
    def get():
        """

        :return: standard HTTP response
        """

        list_o_subscriber_ids = []
        dict_of_subscribers = {}
        with open(FUT.fut_subscribers_file) as fut_fh:
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

    @staticmethod
    def post():
        """

        :return:
        """

        uscc_eng_parser = Common.create_api_parser()
        uscc_eng_parser.add_argument('imsi', location='json')
        args = Common.parse_request_args(uscc_eng_parser)
        list_imsi = args.get('imsi').split(',')
        with open(FUT.fut_subscribers_file, "a") as sfh:
            for imsi in list_imsi:
                sfh.write(imsi + "\n")

        response = jsonify({'fut_msg': 'IMSI(s) successfully added'})
        response.status_code = 201
        return response

    @staticmethod
    def delete():
        """

        :return:
        """

        uscc_eng_parser = Common.create_api_parser()
        uscc_eng_parser.add_argument('imsi', location='json')
        args = Common.parse_request_args(uscc_eng_parser)
        list_imsi = args.get('imsi').split(',')
        with open(FUT.fut_subscribers_file, "r") as sfhr:
            lines = sfhr.readlines()
            sfhr.close()
        with open(FUT.fut_subscribers_file, "w") as sfhw:
            for imsi_delete in list_imsi:
                for imsi in lines:
                    if imsi.strip("\n") != imsi_delete:
                        sfhw.write(imsi)

        response = jsonify({'fut_msg': 'IMSI(s) successfully delete'})
        response.status_code = 200
        return response
