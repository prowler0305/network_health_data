import sys
from flask import jsonify
from flask_restful import Resource
from common.common import Common


class Imsi(Resource):
    """
    """
    try:
        if sys.argv[1] == '--dev':
            imsi_subscribers_file = 'C:\\Users\Owner\IdeaProjects\\uscc_eng_api_personal\\local_test_library\\imsi_test_data'
    except IndexError:
        imsi_subscribers_file = '/opt/app-root/src/data_only/imsi-Subscribers'

    @staticmethod
    def get():
        """

        Retrieves the list of Imsis from the imsi-Subscribers file and formats them as python dictionary

        Example using cURL:

            curl http://localhost:5000/v1/imsis

        :return: list of imsis as a JSON object
        """

        if Common.check_path_exists(Imsi.imsi_subscribers_file):
            list_o_subscriber_ids = []
            dict_of_subscribers = {}
            with open(Imsi.imsi_subscribers_file) as imsi_fh:
                for line in imsi_fh:
                    line = line.rstrip('\n')
                    list_o_subscriber_ids.append(line)

            for list_index in range(len(list_o_subscriber_ids)):
                dict_of_subscribers[list_index] = list_o_subscriber_ids[list_index]

            response = jsonify(dict_of_subscribers)
            response.status_code = 200
        else:
            response = jsonify({'message': "Can't get to file containing subscriber IDs. Please contact Core "
                                           "Automation Team."})
            response.status_code = 500
        return response

    @staticmethod
    def post():
        """
        Looks for the "imsi" parameter to be provided in the body of the POST to add to the imsi-Subscribers file.

        If the file doesn't exist the path/file will be created, else the Imsi(s) will be added to the file on a new
        line.

        A single or comma delimited string of imsis can be provided to be added on a single POST request.

        Examples using cUrl commands:

            Single imsi
                curl -d '{"imsi":"123456789"}' -H "Content-type: application/json" -X POST http://localhost:5000/v1/imsis

            Multiple imsi
                curl -d '{"imsi":"123456789,12346789,123456789"}' -H "Content-type: application/json" -X POST http://localhost:5000/v1/imsis

        List of test Imsis used to test:
        311580704895154
        311580707305677
        311580705520444
        311580702595068
        311580704830154
        311580702594425
        311580704830207
        311580704862845
        311580707592017
        311580705869630
        311580706045064

        :return: Successful - standard HTTP 201 response
                    Failure - HTTP response
        """

        if not Common.check_path_exists(Imsi.imsi_subscribers_file):
            with open(Imsi.imsi_subscribers_file, "w+") as sfhw:
                pass

        uscc_eng_parser = Common.create_api_parser()
        uscc_eng_parser.add_argument('imsi', location='json')
        args = Common.parse_request_args(uscc_eng_parser)
        list_imsi = args.get('imsi').split(',')
        with open(Imsi.imsi_subscribers_file, "r") as sfhr:
            lines = sfhr.readlines()
            sfhr.close()
            with open(Imsi.imsi_subscribers_file, "a") as sfh:
                for imsi in list_imsi:
                    if imsi + '\n' not in lines:
                        sfh.write(imsi + "\n")
                response = jsonify({'imsi_msg': 'IMSI(s) successfully added'})
                response.status_code = 201

        return response

    @staticmethod
    def delete():
        """
        Removes either a single imsi or a comma delimited string of imsis from the imsi-subscribers file.

        A single or comma delimited string of imsis can be provided to be added on a single POST request.

        Examples using cUrl commands:

            Single imsi
                curl -d '{"imsi":"123456789"}' -H "Content-type: application/json" -X DELETE http://localhost:5000/v1/imsis

            Multiple imsi
                curl -d '{"imsi":"123456789,12346789,123456789"}' -H "Content-type: application/json" -X DELETE http://localhost:5000/v1/imsis


        :return: Successful - Standard HTTP 200 response code in JSON format
                    Failure - Error that occurred in JSON response
        """

        if Common.check_path_exists(Imsi.imsi_subscribers_file):
            uscc_eng_parser = Common.create_api_parser()
            uscc_eng_parser.add_argument('imsi', location='json')
            args = Common.parse_request_args(uscc_eng_parser)
            delete_imsi_list = args.get('imsi').split(',')
            with open(Imsi.imsi_subscribers_file, "r") as sfhr:
                lines = sfhr.readlines()
                sfhr.close()
                with open(Imsi.imsi_subscribers_file, "w") as sfhw:
                    for imsi in lines:
                        if imsi.strip('\n') not in delete_imsi_list:
                            sfhw.write(imsi)

                    response = jsonify({'imsi_msg': 'IMSI(s) successfully deleted'})
                    response.status_code = 200
        else:
            response = jsonify({"message": "Can't get to file containing subscriber IDs. Please contact Core "
                                           "Automation Team."})
            response.status_code = 500
        return response
