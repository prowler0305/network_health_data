from flask import jsonify
from flask_restful import Resource
from flask_jwt_simple import jwt_required, get_jwt_identity


class Protected(Resource):
    """
    """

    @staticmethod
    @jwt_required
    def get():
        """
        Protected view with jwt_required, which requires a valid jwt to be present in the header.

        Test using following cURL command after obtain JWT from login method:
            curl -H "Authorization: JWT $ACCESS" http://localhost:5000/jwt_simple/protected

        :return: JSON encoded identity and status code
        """
        # Access the identity of the current user with get_jwt_identity.
        # This is obtained out of the JWT passed by the user.
        response = jsonify({'hello_from': get_jwt_identity()})
        response.status_code = 200
        return response
