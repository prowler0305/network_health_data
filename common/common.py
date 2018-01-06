from flask import jsonify


class Common(object):
    """
    Common class that encapsulates static methods for common functionality.

    """

    @staticmethod
    def generate_error_response(error_msg_key, error_text, response_code):
        """
        Formats a simple error message to be returned in http response as a JSON object.

        :param error_msg_key: string to use as the key in the JSON object error response returned.
        :param error_text: Message text to be returned. It will be sent as a part of a JSON response with the
        "wng_api_msg" key value. (i.e. {"msg_api_msg": "<error_text>"})
        :param response_code: the HTTP response code to be set as the response.status_code
        :return: Error message and status code in a JSON format
        """

        error_response = jsonify({error_msg_key: error_text})
        error_response.status_code = response_code
        return error_response
