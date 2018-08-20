# Flask
from flask import render_template, redirect, request, url_for, abort, make_response
from flask.views import MethodView

# USCC
from resources.logout import Logout
from uscc_api import api, uscc_eng_app
from uscc_apps.dev_container_status.forms import ContainerForm
from common.common import Common

# Misc
import requests
import json
import os


class UpdateContainer(MethodView):
    def __init__(self):

        # self.imsi_header = {'Authorization': None}
        # self.imsi_tracking_dict = dict(imsi=None,
        #                                userid=None,
        #                                email=None
        #                                )
        # self.imsi_list_get_resp = None
        self.login_redirect_response = None
        self.container_status_dict = None

    def get(self):
        """

        :return: Renders the html page with all substituted content needed.
        """
        if request.cookies.get('access_token_cookie') is None:
            self.redirect_to_uscc_login()
            return self.login_redirect_response

        form = ContainerForm()

        return render_template('container_status/update_container_status.html', form=form)

    def post(self):
        """
        """

        if 'logout_btn' in request.form:
            self.delete()
            return self.login_redirect_response

        if request.cookies.get('access_token_cookie') is None:
            self.redirect_to_uscc_login()
            return self.login_redirect_response
        # else:
        #     # INFO: needed if JWT_TOKEN_LOCATION is set to headers as opposed to in cookies
        #     # self.imsi_header['Authorization'] = 'JWT {}'.format(request.cookies.get('access_token_cookie'))
        #     # INFO: With JWT in cookies set the CSRF token is still expected to be in the header for POST to succeed
        #     self.imsi_header['X-CSRF-TOKEN'] = request.cookies.get('csrf_access_token')
        #     self.imsi_header['content_type'] = 'application/json'

        form = ContainerForm()
        if form.validate_on_submit():
            with open(os.environ.get('container_status_path')) as csrfh:
                status_file_dict = json.load(csrfh)

            update_container_dict = status_file_dict.get(request.form.get('container_name'))
            update_container_dict['status'] = 'not open'
            update_container_dict.get('time_frame')['start_date'] = request.form.get('start_date')
            update_container_dict.get('time_frame')['end_date'] = request.form.get('end_date')
            update_container_dict.get('poc')['name'] = request.form.get('poc_name')
            update_container_dict.get('poc')['email'] = request.form.get('poc_email')
            status_file_dict[request.form.get('container_name')] = update_container_dict

            with open(os.environ.get('container_status_path'),mode='w') as cswfh:
                json.dump(status_file_dict, cswfh)
        else:
            if len(form.errors) != 0:
                for form_field, error_message_text in form.errors.items():
                    Common.create_flash_message(message=form_field + ':' + error_message_text[0])

        return render_template('container_status/update_container_status.html', form=form)

    def delete(self):
        """
        Called by the above post() method if the radio button value is 'D' in which an HTTP DELETE request is made to
        the USCC ENG REST API to delete the imsi(s) from the tracking file.

        :return: True - if the delete API request is successful with a successful message
                False - if the delete API request is unsuccessful with an error message derived from the API HTTP
                        Response object.
        """

        if 'logout_btn' in request.form:
            self.imsi_header['X-CSRF-TOKEN'] = request.cookies.get('csrf_access_token')
            imsi_logout_resp = requests.delete(api.url_for(Logout, _external=True), headers=self.imsi_header,
                                               cookies={'access_token_cookie': request.cookies.get('access_token_cookie')})
            if imsi_logout_resp.status_code == requests.codes.ok:
                self.redirect_to_uscc_login()


        else:
            imsi_delete_resp = requests.delete(api.url_for(Imsi, _external=True),
                                               data=json.dumps(self.imsi_tracking_dict),
                                               headers=self.imsi_header,
                                               cookies={'access_token_cookie': request.cookies.get('access_token_cookie')})

            if imsi_delete_resp.status_code == requests.codes.ok:
                Common.create_flash_message(imsi_delete_resp.json().get('imsi_msg'))
                return True
            else:
                if imsi_delete_resp.status_code == requests.codes.unauthorized:
                    self.redirect_to_uscc_login()
                    return self.login_redirect_response
                else:
                    delete_error_message = "%s: %s" % (imsi_delete_resp.status_code, imsi_delete_resp.reason)
                    Common.create_flash_message(delete_error_message, 'error')
                    return False

    def redirect_to_uscc_login(self):
        """
        Redirects to the USCC Login application
        :return: redirect response
        """

        self.login_redirect_response = redirect(os.environ.get('login_app') + '?referrer=' +
                                                url_for('update_container', _external=True))
        return
