from flask import jsonify, request
from flask_restful import Resource
# import requests
# import kerberos
# from requests_kerberos import HTTPKerberosAuth, OPTIONAL


class AuthenticateKerberos(Resource):
    @staticmethod
    def post():
        """
        Authentication Method to access data sources that are behind the Kerberos authentication server mechanism.

        This method is accessed by doing a http POST request receiving the username and password credentials of the end
        user accessing the data. These credentials are used to authenticate the end user in the Kerberos auth database.

        If the user is identified then a Kerberos authentication token is returned. This token needs saved and sent on
        all subsequent data GET requests.

        :return: Kerberos auth token
        """
        if not request.is_json:
            response = jsonify({'msg': 'Missing JSON in request'})
            response.status_code = 400
            # return response

        auth_params = request.get_json()
        username = auth_params.get('username')
        password = auth_params.get('password')

        if not username:
            response = jsonify({'msg': 'Missing username parameter'})
            response.status_code = 400
            # return response
        if not password:
            response = jsonify({'msg': 'Missing password parameter'})
            response.status_code = 400
            # return response

        # # Todo: insert Kerberos authentication integration code here
        # rc, krb_context = kerberos.authGSSClientInit("HTTP://ilscha03-hden-01.uscc.com@INT.USC.LOCAL")
        # kerberos.authGSSClientStep(krb_context, "")
        # negotiate_details = kerberos.authGSSClientResponse(krb_context)
        # print(negotiate_details)
        # wng_auth_header = {"Authorization": "Negotiate" + negotiate_details}
        # hbase_base_url = "http://ilscha03-hden-01.uscc.com:20550/"
        # r = requests.get(hbase_base_url, headers=wng_auth_header, verify=False)
        # print(r.status_code)
        # print(r)
        if username != 'aspea002' or password != 'test':
            response = jsonify({'msg': 'Bad username or password'})
            response.status_code = 401
        else:
            # Identity can be any data that is json serializable
            response = jsonify({'kerb_token': 'my Kerberos auth token'})
            response.status_code = 200

        return response
