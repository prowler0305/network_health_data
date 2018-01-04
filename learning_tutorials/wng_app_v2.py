import datetime
from flask import Flask
from flask_restful import Api
from resources.jwt_ext_protected import Protected
from resources.auth import Authenticate
from resources.refresh import Refresh
from flask_jwt_extended import JWTManager


app = Flask(__name__)
# App configuration is for use with FLASK JWT authentication. Which is not in use currently as the HBASE API access uses
# the Kerboso authentication mechanism.
# TODO: SECRET_KEY - digitally-sign for the JWT token. This needs to be more difficult. Maybe a random generated string?
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_HEADER_TYPE'] = 'JWT'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=20)
jwt = JWTManager(app)
api = Api(app)

api.add_resource(Authenticate, '/login')
api.add_resource(Refresh, '/refresh_token')
api.add_resource(Protected, '/protected')

if __name__ == '__main__':
    app.run(debug=True)
