import requests
from flask import flash, json
from requests import Response


class Common(object):
    """
    Class of static method to provide generic or common functionality to be used across all apps contained in the
    uscc_apps directory.
    """

    @staticmethod
    def create_flash_message(message=None, category_request=None):
        """
        Creates a flask flash message object that can be used on the next HTTP request.

        :param message: Can be a string or an HTTP response object in which the response text which should contain the
        standard HTTP error text will be extracted as the message
        :param category_request: category of the message as documented in flask.helpers.flash()
        :return: Flash object that was created.
        """

        if isinstance(message, Response):
            if 'message' in message:
                message_dict = json.loads(message)
            else:
                message_dict = dict(message=None)
                message_dict['message'] = str(message.status_code) + ':' + message.reason
            return flash(message_dict['message'], category=category_request)
        else:
            return flash(message, category=category_request)

    @staticmethod
    def unauthorized_error(response_obj):
        """
        Accesses and returns the unauthorized error message an HTTP response object that contains an Unauthorized status
         code from the USCC Engineering API

        :param response_obj: http response object
        :return: error message text or if response_obj is not a 401 or the text does not contain a msg key in json
        string then None
        """
        if response_obj.status_code == requests.codes.unauthorized:
            error_message_dict = json.loads(response_obj.text)
            return error_message_dict.get('msg')
        else:
            return None
