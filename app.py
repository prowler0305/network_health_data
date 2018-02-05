import sys
# from flask import Flask, render_template, flash, redirect
from flask import Flask
from flask_restful import Api
from resources.list_all import ListAll
from resources.table_action import TableAction
from resources.row_query import RowQuery
from resources.site_map import SiteMap
from resources.scanning import Scanning
from resources.imsi import Imsi
from uscc_apps.imsi_tracking.imsi_tracking import ImsiTracking
# from resources.auth_kerb import AuthenticateKerberos
# from resources.auth import Authenticate
# from resources.refresh import Refresh
# from flask_jwt_extended import JWTManager


uscc_eng_app = Flask(__name__)
uscc_eng_app.config['SECRET_KEY'] = 'you-will-never-guess'
# App configuration is for use with FLASK JWT authentication. Which is not in use currently as the HBASE API access uses
# the Kerboso authentication mechanism. Once the need for API Athentication via JWT is needed this code and the
# associated import statements will need to be uncommented.
# TODO: SECRET_KEY - digitally-sign for the JWT token. This needs to be more difficult. Maybe a random generated string?
# app.config['JWT_SECRET_KEY'] = 'super-secret'
# app.config['JWT_HEADER_TYPE'] = 'JWT'
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=20)
# jwt = JWTManager(app)
api = Api(uscc_eng_app, prefix='/v1')


# Add resources via the add_resource method

# api.add_resource(Authenticate, '/login')
# api.add_resource(Refresh, '/refresh_token')
# api.add_resource(AuthenticateKerberos, '/auth')
api.add_resource(SiteMap, '/')
api.add_resource(ListAll, '/list_all')
api.add_resource(TableAction, '/action')
api.add_resource(RowQuery, '/row_query')
api.add_resource(Scanning, '/scan')
api.add_resource(Imsi, '/imsis')

imsi_view = ImsiTracking.as_view(name='imsi_tracking')
uscc_eng_app.add_url_rule('/track-imsi', view_func=imsi_view, methods=['POST', 'GET'])


if __name__ == '__main__':
    try:
        if sys.argv[1] == '--dev':
            uscc_eng_app.run(debug=True, threaded=True)
    except IndexError:
        uscc_eng_app.run(host='0.0.0.0', port=8080)
