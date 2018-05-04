# Flask
from flask import render_template, redirect, request, url_for
from flask.views import MethodView

# USCC
from uscc_apps.uscc_login.login_form import LoginForm
from uscc_apps.common import Common

# Misc
import requests
import json
import sys
import os


class Login(MethodView):
    def __init__(self):
        self.headers = {'content-type': 'application/json'}
        self.auth_data = dict(username=None, password=None)
        self.auth_url = os.environ.get('auth_api_url')

    def get(self):
        """

        :return:
        """

        form = LoginForm()

        return render_template('login.html', form=form)

    def post(self):
        """

        """

        form = LoginForm()
        if form.validate_on_submit():
            self.auth_data['username'] = request.form['username']
            self.auth_data['password'] = request.form['password']
            auth_response = requests.post(self.auth_url, data=json.dumps(self.auth_data), headers=self.headers)
            if auth_response.status_code == requests.codes.ok:
                auth_token = json.loads(auth_response.text)
                return redirect(url_for('imsi_tracking', art=auth_token.get('access_token'),
                                        userid=self.auth_data.get('username'))
                                )
            elif auth_response.status_code == requests.codes.unauthorized:
                bad_cred_mmsg = 'Username and/or password is invalid. Please reenter.'
                Common.create_flash_message(bad_cred_mmsg)
            else:
                Common.create_flash_message(auth_response)
        else:
            if len(form.errors) != 0:
                for error_message_text in form.errors.values():
                    Common.create_flash_message(error_message_text[0])

        return render_template('login.html', form=form)
