from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

# Example of protecting a resource with Flask_JWT_extended. This is currently not being used by the USCC Engineering API API as we are
# using kerberos authentication.


class Protected(Resource):
    """
    """

    @staticmethod
    @jwt_required
    def get():
        """
        Protected view with jwt_required, which requires a valid jwt to be present in the header.

        Test using following cURL command after obtain JWT from login method:
        Linux:
            curl -H "Authorization: JWT $ACCESS" http://localhost:5000/jwt_ext/protected
        Windows:
            curl -H "Authorization: JWT %access%" http://localhost:5000/jwt_ext/protected

        :return: JSON encoded identity and status code
        """
        # Access the identity of the current user with get_jwt_identity.
        # This is obtained out of the JWT passed by the user.
        current_user = get_jwt_identity()
        response = jsonify(logged_in_as=current_user)
        response.status_code = 200
        return response
