import datetime
from flask import Flask
from flask_restful import Api
from resources.protected import Protected
from resources.auth import Authenticate
from flask_jwt_simple import JWTManager


app = Flask(__name__)
# TODO: SECRET_KEY - digitally-sign for the JWT token. This needs to be more difficult. Maybe a random generated string?
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_HEADER_TYPE'] = 'JWT'
app.config['JWT_EXPIRES'] = datetime.timedelta(minutes=5)
jwt = JWTManager(app)
api = Api(app, prefix='/jwt_simple')

api.add_resource(Authenticate, '/login')
api.add_resource(Protected, '/protected')

if __name__ == '__main__':
    app.run(debug=True)
