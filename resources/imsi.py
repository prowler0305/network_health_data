import sys
import os
from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from common.common import Common


class Imsi(Resource):
    """
    """
    try:
        if sys.argv[1] == '--dev':
            imsi_subscribers_file = 'local_test_library/imsi_test_data_'
    except IndexError:
        imsi_subscribers_file = '/opt/app-root/src/data_only/imsi-Subscribers-'

    @staticmethod
    @jwt_required
    def get():
        """

        Retrieves the list of Imsis from the imsi-Subscribers file and formats them as python dictionary

        Example using cURL:

            curl http://localhost:5000/v1/imsis

        Protected view with jwt_required, which requires a valid JWT to be present in the header.

        Example using cURL command after obtain JWT from login method which is in a local variable "ACCESS":
        Linux:
            curl -H "Authorization: JWT $ACCESS" http://localhost:5000/v1/login
        Windows:
            curl -H "Authorization: JWT %access%" http://localhost:5000/v1/login

        :return: list of imsis as a JSON object
        """

        imsi_parser = Common.create_api_parser()
        imsi_parser.add_argument('no_alias', choices=['true', 'false'])
        imsi_parser.add_argument('userid', required=True)
        imsi_get_args = Common.parse_request_args(imsi_parser)
        imsi_file_path = Imsi.imsi_subscribers_file + imsi_get_args.get('userid')
        email_pos = 0
        return_dict = dict(imsi_list=None, email_list=None)
        if Common.check_path_exists(imsi_file_path):
            list_o_subscriber_ids = []
            list_o_emails = []
            dict_of_subscribers = {}
            dict_of_emails = {}
            with open(imsi_file_path) as imsi_fh:
                current_pos = 0
                for line in imsi_fh:
                    current_pos = current_pos + len(line) + 1
                    if '=' not in line:
                        if imsi_get_args.get('no_alias') == 'true':
                            if '(' in line:
                                imsi, alias_right_paren = line.split('(', 1)
                                list_o_subscriber_ids.append(imsi)
                            else:
                                line = line.rstrip('\n')
                                list_o_subscriber_ids.append(line)
                        else:
                            line = line.rstrip('\n')
                            list_o_subscriber_ids.append(line)
                    else:
                        email_pos = current_pos
                        break

            if email_pos != 0:
                with open(imsi_file_path) as email_fh:
                    email_fh.seek(email_pos)
                    for line in email_fh:
                        line = line.rstrip('\n')
                        list_o_emails.append(line)

            for list_index in range(len(list_o_subscriber_ids)):
                dict_of_subscribers[list_index] = list_o_subscriber_ids[list_index]
            for list_index in range(len(list_o_emails)):
                dict_of_emails[list_index] = list_o_emails[list_index]

            return_dict['imsi_list'] = dict_of_subscribers
            return_dict['email_list'] = dict_of_emails

            response = jsonify(return_dict)
            response.status_code = 200
        else:
            response = jsonify({"message": "File doesn't exist yet. Add an Imsi to create the File."})
            response.status_code = 204

        return response

    @staticmethod
    @jwt_required
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

        uscc_eng_parser = Common.create_api_parser()
        uscc_eng_parser.add_argument('imsi', location='json')
        uscc_eng_parser.add_argument('userid', location='json')
        uscc_eng_parser.add_argument('email', location='json')
        args = Common.parse_request_args(uscc_eng_parser)
        imsi_file_path = Imsi.imsi_subscribers_file + args.get('userid')
        add_response_dict = dict(add_imsi_msg=None, add_email_msg=None)

        # If the tracking file doesn't exist then create it
        if not Common.check_path_exists(imsi_file_path):
            with open(imsi_file_path, "w+") as sfhw:
                pass

        if args.get('imsi') is not None:
            args['imsi'] = args.get('imsi').replace(' ', '')
            list_imsi = args.get('imsi').split(',')
            with open(imsi_file_path, "r") as sfhr:
                lines = sfhr.readlines()
                sfhr.close()
                with open(imsi_file_path, "a") as sfh:
                    for imsi in list_imsi:
                        if imsi + '\n' not in lines:
                            sfh.write(imsi + "\n")
                            add_response_dict['add_imsi_msg'] = 'IMSI(s) successfully added'
                            # response = jsonify(add_response_dict)
                            # response.status_code = 201

        if args.get('email') is not None:
            with open(imsi_file_path, "r") as email_fh:
                content = email_fh.read()
                file_sep_index = content.index('=')
                sep_content = content[file_sep_index]
                email_content_start = file_sep_index + len(sep_content) + 4
                email_fh.seek(email_content_start)
                email_content = email_fh.readlines()
                email_fh.close()
                for email in email_content:
                    email_index = email_content.index(email)
                    email_content[email_index] = email.strip('\n')
                with open(imsi_file_path, "a") as email_afh:
                    if args.get('email') not in email_content:
                        email_afh.write(args.get('email') + '\n')
                        add_response_dict['add_email_msg'] = 'Email successfully added'
                        # response = jsonify(add_response_dict)
                        # response.status_code = 201

        response = jsonify(add_response_dict)
        response.status_code = 201

        return response

    @staticmethod
    @jwt_required
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

        uscc_eng_parser = Common.create_api_parser()
        uscc_eng_parser.add_argument('imsi', location='json')
        uscc_eng_parser.add_argument('userid', location='json')
        uscc_eng_parser.add_argument('email', location='json')
        args = Common.parse_request_args(uscc_eng_parser)
        imsi_file_path = Imsi.imsi_subscribers_file + args.get('userid')

        if Common.check_path_exists(imsi_file_path):
            args['imsi'] = args.get('imsi').replace(' ', '')
            delete_imsi_list = args.get('imsi').split(',')
            with open(imsi_file_path, "r") as sfhr:
                lines = sfhr.readlines()
                sfhr.close()
                with open(imsi_file_path, "w") as sfhw:
                    for line in lines:
                        if '(' in line:
                            imsi, junk = line.split('(', 1)
                            imsi = imsi + '\n'  # Make imsi variable look like one that wasn't provided with an alias.
                        else:
                            imsi = line

                        if imsi.strip('\n') not in delete_imsi_list:
                            sfhw.write(line)

                    response = jsonify({'imsi_msg': 'IMSI(s) successfully deleted'})
                    response.status_code = 200
        else:
            response = jsonify({"message": "Can't get to file containing subscriber IDs. Please contact Core "
                                           "Automation Team."})
            response.status_code = 500
        return response
