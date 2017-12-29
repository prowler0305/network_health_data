import datetime
from flask import Flask
from flask_restful import Api
from resources.jwt_ext_protected import Protected
from resources.auth_refresh import Authenticate
from flask_jwt_extended import JWTManager


app = Flask(__name__)
# TODO: SECRET_KEY - digitally-sign for the JWT token. This needs to be more difficult. Maybe a random generated string?
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_HEADER_TYPE'] = 'JWT'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=1)
jwt = JWTManager(app)
api = Api(app, prefix='/jwt_ext')

api.add_resource(Authenticate, '/login')
api.add_resource(Authenticate, '/refresh_token', endpoint='refresh')
api.add_resource(Protected, '/protected')

if __name__ == '__main__':
    app.run(debug=True)
