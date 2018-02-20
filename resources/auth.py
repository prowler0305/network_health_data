from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity


# This Authentication resource is currently not in use as the USCC Engineering API data is controlled using kerberos authentication. See
# class: AuthenticateKerberos in py file: auth_kerb.py.

class Authenticate(Resource):
    @staticmethod
    def post():
        """
        Method to create both access and refresh tokens.

        The create_access_token() creates the JWT access token which has a short lifespan. The create_refresh_token()
        creates a refresh token with a longer life span so that users can refresh their access token when it expires.

        Test using following cURL command after obtain JWT from login method:
            Linux(syntax):
                curl -H "content-type: application/json" -X POST -d '{"username":"test","password":"test"}' http://localhost:5000/v1/login
            Windows(syntax):
                curl -H "Content-Type: application/json" -X POST http://localhost:5000/v1/login -d "{\"username\":\"test\",\"password\":\"test\"}"
        :return:
        """
        api_cred_path = 'C:\\Users\\Owner\\IdeaProjects\\uscc_eng_api_personal\\local_test_library\\api_cred'

        if not request.is_json:
            response = jsonify({'msg': 'Missing JSON in request'})
            response.status_code = 400
            return response

        params = request.get_json()
        user_name = params.get('username')
        user_password = params.get('password')

        if not user_name:
            response = jsonify({'msg': 'Missing username parameter'})
            response.status_code = 400
            return response
        if not user_password:
            response = jsonify({'msg': 'Missing password parameter'})
            response.status_code = 400
            return response

        with open(api_cred_path) as afh:
            for line in afh:
                file_userid, file_password = line.split('=')
                if file_userid == user_name and file_password.strip('\n') == user_password:
                    # Identity can be any data that is json serializable
                    art = {
                        'access_token': create_access_token(identity=user_name),
                        'refresh_token': create_refresh_token(identity=user_name)}
                    response = jsonify(art)
                    response.status_code = 200
                    return response

        response = jsonify({'msg': 'Bad username or password'})
        response.status_code = 401
        return response
