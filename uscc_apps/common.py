from flask import flash
from requests import Response


class Common(object):
    """
    Class of static method to provide generic or common functionality to be used across all apps contained in the
    uscc_apps directory.
    """

    @staticmethod
    def create_flash_message(message=None, category_request=None):
        """
        Creates a flask flash message object that can be used on the next request.

        :param message: Can be a string or an HTTP response object in which the response text which should contain the
        standard HTTP error text will be extracted as the message
        :param category_request: category of the message as documented in flask.helpers.flash()
        :return: Flash object that was created.
        """

        if isinstance(message, Response):
            message_dict = message.json()
            return flash(message_dict['message'], category=category_request)
        else:
            return flash(message, category=category_request)
