# Flask
from flask import render_template, flash, redirect, request
from flask.views import MethodView

# USCC
from uscc_apps.imsi_tracking.forms import ImsiForm
from uscc_apps.common import Common

# Misc
import requests
import json
import sys


class ImsiTracking(MethodView):
    def __init__(self):

        try:
            if sys.argv[1] == '--dev':
                self.imsi_tracking_api_url = 'http://localhost:5000/v1/imsis'
        except IndexError:
            self.imsi_tracking_api_url = 'http://www.uscc-eng-api.devengos.uscc.com/v1/imsis'

        self.imsi_header = {'content-type': 'application/json'}
        self.imsi_tracking_dict = dict(imsi=None)

    def get(self):
        """

        :return:
        """

        form = ImsiForm()
        imsi_list = {}
        imsi_list_get_resp = requests.get(self.imsi_tracking_api_url)
        if imsi_list_get_resp.status_code == requests.codes.ok:
            imsi_list = imsi_list_get_resp.json()
        else:
            Common.create_flash_message(imsi_list_get_resp)

        return render_template('imsi_tracking/imsi_tracking.html', form=form, imsi_list=imsi_list)

    def post(self):
        """

        :return:
        """

        form = ImsiForm()
        if form.validate_on_submit():
            self.imsi_tracking_dict['imsi'] = request.form['imsis']
            if request.form['add_delete_radio'] == 'A':
                imsi_post_resp = \
                    requests.post(self.imsi_tracking_api_url, data=json.dumps(self.imsi_tracking_dict),
                                  headers=self.imsi_header)
                if imsi_post_resp.status_code == requests.codes.created:
                    Common.create_flash_message('Imsi(s) successfully added')
                else:
                    Common.create_flash_message(imsi_post_resp)
                return redirect('/track-imsi')
            else:
                self.delete()
                return redirect('/track-imsi')
        else:
            if len(form.errors) != 0:
                for error_message_text in form.errors.values():
                    Common.create_flash_message(error_message_text[0])

        return render_template('imsi_tracking/imsi_tracking.html', form=form)

    def delete(self):
        """

        :return:
        """

        imsi_delete_resp = requests.delete(self.imsi_tracking_api_url, data=json.dumps(self.imsi_tracking_dict),
                                           headers=self.imsi_header)
        if imsi_delete_resp.status_code == requests.codes.ok:
            Common.create_flash_message('Imsi(s) successfully deleted')
            return True
        else:
            Common.create_flash_message(imsi_delete_resp)
            return False

