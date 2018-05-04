import datetime
import os
from flask import Flask
from flask_restful import Api
from resources.list_all import ListAll
from resources.table_action import TableAction
from resources.row_query import RowQuery
from resources.site_map import SiteMap
from resources.scanning import Scanning
from resources.imsi import Imsi
from uscc_apps.imsi_tracking.imsi_tracking import ImsiTracking
from uscc_apps.uscc_login.uscc_app_login import *
# from resources.auth_kerb import AuthenticateKerberos
from resources.auth import Authenticate
from resources.refresh import Refresh
from resources.volte_load import VolteLoad
from flask_jwt_extended import JWTManager


uscc_eng_app = Flask(__name__)
uscc_eng_app.config['SECRET_KEY'] = 'you-will-never-guess'
# TODO: SECRET_KEY - digitally-sign for the JWT token. This needs to be more difficult. Maybe a random generated string?
uscc_eng_app.config['JWT_SECRET_KEY'] = 'super-secret'
uscc_eng_app.config['JWT_HEADER_TYPE'] = 'JWT'
if os.environ.get('propagate_excps') == 'True':
    uscc_eng_app.config['PROPAGATE_EXCEPTIONS'] = True
else:
    uscc_eng_app.config['PROPAGATE_EXCEPTIONS'] = False

if os.environ.get('access_token_expiration') is not None:
    uscc_eng_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=int(os.environ.get('access_token_expiration')))

if os.environ.get('refresh_token_expiration') is not None:
    uscc_eng_app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(seconds=int(os.environ.get('refresh_token_expiration')))

jwt = JWTManager(uscc_eng_app)
api = Api(uscc_eng_app, prefix='/v1')


# Add resources via the add_resource method

api.add_resource(Authenticate, '/login')
api.add_resource(Refresh, '/refresh_token')
# api.add_resource(AuthenticateKerberos, '/auth')
api.add_resource(SiteMap, '/')
api.add_resource(ListAll, '/list_all')
api.add_resource(TableAction, '/action')
api.add_resource(RowQuery, '/row_query')
api.add_resource(Scanning, '/scan')
api.add_resource(Imsi, '/imsis')
api.add_resource(VolteLoad, '/volte_load')

imsi_view = ImsiTracking.as_view(name='imsi_tracking')
login_view = Login.as_view(name='uscc_login')
uscc_eng_app.add_url_rule('/track-imsi', view_func=imsi_view, methods=['POST', 'GET'])
uscc_eng_app.add_url_rule('/login', view_func=login_view, methods=['POST', 'GET'])


if __name__ == '__main__':

    print(os.environ.get('local_execution'))
    if os.environ.get('local_execution') is not None:
        print("I'm going to run in debug mode")
        uscc_eng_app.run(debug=True, threaded=True)
    else:
        uscc_eng_app.run(host='0.0.0.0', port=8080, threaded=True)
