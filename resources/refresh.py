from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_refresh_token_required, get_jwt_identity

# This Authentication resource is currently not in use as the USCC Engineering API data is controlled using kerberos authentication. See
# class: AuthenticateKerberos in py file: auth_kerb.py.


class Refresh(Resource):
    @staticmethod
    @jwt_refresh_token_required
    def get():
        """
        Method to re-issue an access token. This is only possible if the user has a valid refresh token that is issued
        by the class: Authenticate: py: login method.

        Test using following cURL command after obtain JWT from login method:
            Linux(syntax):
                curl -H "Authorization: JWT $refresh http://localhost:5000/jwt_ext/refresh_token
            Windows(syntax):
                curl -H "Authorization: JWT %refresh%" http://localhost:5000/jwt_ext/refresh_token
        :return:
        """
        current_user = get_jwt_identity()
        nat = {
            'access_token': create_access_token(identity=current_user)
        }

        response = jsonify(nat)
        response.status_code = 200
        return response
