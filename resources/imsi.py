import sys
import os
from flask import jsonify, make_response, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from common.common import Common


class Imsi(Resource):
    """
    """
    # noinspection PyTypeChecker
    imsi_subscribers_file = os.environ.get('imsi_file_path')
    # noinspection PyTypeChecker
    email_address_file = os.environ.get('email_file_path')

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
        email_file_path = Imsi.email_address_file + imsi_get_args.get('userid')
        return_dict = dict(imsi_list=None, email_list=None)
        no_imsi_yet = {0: "No Imsi(s) being tracked yet."}
        no_email_yet = {0: "No email addresses added yet."}

        if Common.check_path_exists(imsi_file_path):
            list_o_subscriber_ids = []
            dict_of_subscribers = {}

            with open(imsi_file_path, "r") as imsi_fh:
                # current_pos = 0
                for line in imsi_fh:
                    # current_pos = current_pos + len(line)
                    # if '=' not in line:
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

            for list_index in range(len(list_o_subscriber_ids)):
                dict_of_subscribers[list_index] = list_o_subscriber_ids[list_index]

            return_dict['imsi_list'] = dict_of_subscribers
        else:
            return_dict['imsi_list'] = no_imsi_yet

        if Common.check_path_exists(email_file_path):
            list_o_emails = []
            dict_of_emails = {}
            with open(email_file_path, "r") as email_fh:
                for line in email_fh:
                    line = line.rstrip('\n')
                    list_o_emails.append(line)

            for list_index in range(len(list_o_emails)):
                dict_of_emails[list_index] = list_o_emails[list_index]

            return_dict['email_list'] = dict_of_emails
        else:
            return_dict['email_list'] = no_email_yet

        if len(return_dict.get('imsi_list')) > 0 and len(return_dict.get('email_list')) > 0:
            response = jsonify(return_dict)

        elif len(return_dict.get('imsi_list')) == 0 and len(return_dict.get('email_list')) > 0:
            return_dict['imsi_list'] = no_imsi_yet
            response = jsonify(return_dict)

        elif len(return_dict.get('email_list')) == 0 and len(return_dict.get('imsi_list')) > 0:
            return_dict['email_list'] = no_email_yet
            response = jsonify(return_dict)

        else:
            return_dict['imsi_list'] = no_imsi_yet
            return_dict['email_list'] = no_email_yet
            response = jsonify(return_dict)

        response.status_code = 200

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
        email_file_path = Imsi.email_address_file + args.get('userid')
        add_resp_dictionary = dict(imsi_msg=None)
        add_imsi = False
        add_email = False

        # If the tracking files don't exist then create them
        if not Common.check_path_exists(imsi_file_path):
            with open(imsi_file_path, "w+") as sfhw:
                pass

        if not Common.check_path_exists(email_file_path):
            with open(email_file_path, "w+") as sfhw:
                pass

        if args.get('imsi') != '':
            args['imsi'] = args.get('imsi').replace(' ', '')
            list_imsi = args.get('imsi').split(',')
            with open(imsi_file_path, "r") as sfhr:
                lines = sfhr.readlines()
                # Strip all alias out of lines list so only the Imsis exist in list object
                for index, line in enumerate(lines):
                    if '(' in line:
                        only_imsi, junk = line.split('(', 1)
                        lines[index] = only_imsi
                    else:
                        lines[index] = line.rstrip('\n')
                sfhr.close()
                with open(imsi_file_path, "a") as afh:
                    for imsi in list_imsi:
                        if imsi.split('(', 1)[0] not in lines:
                            afh.write(imsi + "\n")
                        add_imsi = True

        if args.get('email') != '':
            with open(email_file_path, "r") as email_fh:
                emails = email_fh.readlines()
                email_fh.close()
                with open(email_file_path, "a") as email_afh:
                    if args.get('email') + '\n' not in emails:
                        email_afh.write(args.get('email') + '\n')
                    add_email = True

        if add_imsi:
            add_resp_dictionary['imsi_msg'] = 'IMSI(s)'
            if add_email:
                add_resp_dictionary['imsi_msg'] = add_resp_dictionary.get('imsi_msg') + 'and email successfully added'
                response = jsonify(add_resp_dictionary)
                response.status_code = 201
                return response
            else:
                add_resp_dictionary['imsi_msg'] = add_resp_dictionary.get('imsi_msg') + 'successfully added'
                response = jsonify(add_resp_dictionary)
                response.status_code = 201
                return response
        elif add_email:
            add_resp_dictionary['imsi_msg'] = 'Email successfully added'
            response = jsonify(add_resp_dictionary)
            response.status_code = 201
            return response
        else:
            add_resp_dictionary['imsi_msg'] = 'Error adding IMSI(s) and/or email. Contact Core Automation Team'
            response = jsonify(add_resp_dictionary)
            response.status_code = 500
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
        email_file_path = Imsi.email_address_file + args.get('userid')
        delete_resp_dictionary = dict(imsi_msg='')
        delete_imsi = False
        delete_email = False
        imsi_file_exist = False
        email_file_exist = False

        if args.get('imsi') != '':
            if Common.check_path_exists(imsi_file_path):
                imsi_file_exist = True
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

                        delete_imsi = True

        if args.get('email') != '':
            if Common.check_path_exists(email_file_path):
                email_file_exist = True
                with open(email_file_path, "r") as erfhr:
                    lines = erfhr.readlines()
                    erfhr.close()
                    if len(lines) > 0:
                        try:
                            lines.remove(args.get('email') + '\n')
                            delete_email = True
                        except ValueError:
                            pass
                        with open(email_file_path, "w") as ewfhr:
                            for line in lines:
                                ewfhr.write(line)

        if delete_imsi:
            delete_resp_dictionary['imsi_msg'] = 'IMSI(s)'
            if delete_email:
                delete_resp_dictionary['imsi_msg'] = delete_resp_dictionary.get('imsi_msg') + 'and email successfully deleted'
                response = jsonify(delete_resp_dictionary)
                response.status_code = 200
                return response
            else:
                delete_resp_dictionary['imsi_msg'] = delete_resp_dictionary.get('imsi_msg') + 'successfully deleted.'
                response = jsonify(delete_resp_dictionary)
                response.status_code = 200
                return response
        elif delete_email:
            delete_resp_dictionary['imsi_msg'] = delete_resp_dictionary.get('imsi_msg') + 'Email successfully deleted.'
            response = jsonify(delete_resp_dictionary)
            response.status_code = 200
            return response
        else:
            if not imsi_file_exist or not email_file_exist:
                response = make_response('', 204)
                response.mimetype = current_app.config['JSONIFY_MIMETYPE']
                return response

            else:
                delete_resp_dictionary['imsi_msg'] = delete_resp_dictionary.get('imsi_msg') + \
                                                     'Error deleting IMSI(s) and/or email. Contact Core Automation Team.'
                response = jsonify(delete_resp_dictionary)
                response.status_code = 500
                return response
