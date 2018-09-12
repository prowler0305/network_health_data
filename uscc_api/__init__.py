import os
from flask import Flask, url_for
from flask_restful import Api
from flask_jwt_extended import JWTManager

uscc_eng_app = Flask(__name__)
uscc_eng_app.config.from_object(os.environ.get('app_env'))
jwt = JWTManager(uscc_eng_app)
api = Api(uscc_eng_app, prefix='/v1')
blacklist = set()
# from resources.list_all import ListAll
# from resources.table_action import TableAction
# from resources.row_query import RowQuery
from resources.site_map import SiteMap
# from resources.scanning import Scanning
# from resources.imsi import Imsi
# from uscc_apps.imsi_tracking.imsi_tracking import ImsiTracking
from uscc_apps.uscc_login.uscc_app_login import *
# from resources.auth_kerb import AuthenticateKerberos
from resources.auth import Authenticate
from resources.refresh import Refresh
# from resources.volte_load import VolteLoad
from resources.logout import Logout
from uscc_apps.network_health.ne_health_sms import NeText
from uscc_apps.network_health.nh_dashboard import NetworkHealthDashboard
from resources.sms import Sms

# Add resources via the add_resource method
api.add_resource(Authenticate, '/login')
api.add_resource(Refresh, '/refresh_token')
api.add_resource(Logout, 'logout')
# api.add_resource(SmsNum, '/sms')
# api.add_resource(AuthenticateKerberos, '/auth')
# api.add_resource(SiteMap, '/')
# api.add_resource(ListAll, '/list_all')
# api.add_resource(TableAction, '/action')
# api.add_resource(RowQuery, '/row_query')
# api.add_resource(Scanning, '/scan')
# api.add_resource(Imsi, '/imsis')
# api.add_resource(VolteLoad, '/volte_load')

network_health_text = NeText.as_view(name='ne_text')
network_health_dashboard = NetworkHealthDashboard.as_view(name='nh_dashboard')
login_view = Login.as_view(name='uscc_login')
uscc_eng_app.add_url_rule('/sms_register', view_func=network_health_text, methods=['GET', 'POST'])
uscc_eng_app.add_url_rule('/network_health', view_func=network_health_dashboard, methods=['GET'])
uscc_eng_app.add_url_rule('/login', view_func=login_view, methods=['POST', 'GET'])
