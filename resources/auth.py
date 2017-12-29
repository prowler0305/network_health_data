from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_simple import create_jwt


class Authenticate(Resource):
    @staticmethod
    def post():
        """
        Method to create access tokens. The create_jwt() function is used to actually generate the token

        Test using following cURL command after obtain JWT from login method:
            curl -H "content-type: application/json" -X POST -d '{"username":"test","password":"test"}' http://localhost:5000/jwt_simple/login
        :return:
        """
        if not request.is_json:
            response = jsonify({'msg': 'Missing JSON in request'})
            response.status_code = 400
            return response

        params = request.get_json()
        username = params.get('username')
        password = params.get('password')

        if not username:
            response = jsonify({'msg': 'Missing username parameter'})
            response.status_code = 400
            return response
        if not password:
            response = jsonify({'msg': 'Missing password parameter'})
            response.status_code = 400
            return response

        if username != 'test' or password != 'test':
            response = jsonify({'msg': 'Bad username or password'})
            response.status_code = 401
            return response

        # Identity can be any data that is json serializable
        ret = {'jwt': create_jwt(identity=username)}
        print(ret)
        response = jsonify(ret)
        response.status_code = 200
        return response
