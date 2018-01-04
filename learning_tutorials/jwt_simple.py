import datetime
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_jwt_simple import JWTManager, jwt_required, create_jwt, get_jwt_identity


app = Flask(__name__)
# TODO: SECRET_KEY - digitally-sign for the JWT token. This needs to be more difficult. Maybe a random generated string?
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_HEADER_TYPE'] = 'JWT'
app.config['JWT_EXPIRES'] = datetime.timedelta(minutes=5)
jwt = JWTManager(app)
api = Api(app, prefix='/jwt_simple')


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

api.add_resource(Authenticate, '/login')
api.add_resource(Protected, '/protected')

if __name__ == '__main__':
    app.run(debug=True)


