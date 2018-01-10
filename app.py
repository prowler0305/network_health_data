# import datetime
import sys
from flask import Flask
from flask_restful import Api
# from resources.uscc_eng_parser_api_manager import WngApiManager
from resources.list_all import ListAll
from resources.table_action import TableAction
from resources.row_query import RowQuery
# from resources.auth_kerb import AuthenticateKerberos
# from resources.auth import Authenticate
# from resources.refresh import Refresh
# from flask_jwt_extended import JWTManager


uscc_eng_app = Flask(__name__)
# App configuration is for use with FLASK JWT authentication. Which is not in use currently as the HBASE API access uses
# the Kerboso authentication mechanism. Once the need for API Athentication via JWT is needed this code and the
# associated import statements will need to be uncommented.
# TODO: SECRET_KEY - digitally-sign for the JWT token. This needs to be more difficult. Maybe a random generated string?
# app.config['JWT_SECRET_KEY'] = 'super-secret'
# app.config['JWT_HEADER_TYPE'] = 'JWT'
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=20)
# jwt = JWTManager(app)
api = Api(uscc_eng_app)


# Add resources via the add_resource method

# api.add_resource(Authenticate, '/login')
# api.add_resource(Refresh, '/refresh_token')
# api.add_resource(AuthenticateKerberos, '/auth')
# api.add_resource(WngApiManager, '/uscc_eng_parser_api')
api.add_resource(ListAll, '/uscc_eng_api/list_all')
api.add_resource(TableAction, '/uscc_eng_api/action')
api.add_resource(RowQuery, '/uscc_eng_api/row_query')
# TODO: separate the hbase_keyword parameter into separate API endpoints?
# /list_all
# /action
# /table

if __name__ == '__main__':
    try:
        if sys.argv[1] == '--dev':
            uscc_eng_app.run(debug=True)
    except IndexError:
        uscc_eng_app.run(host='0.0.0.0', port=8080)
