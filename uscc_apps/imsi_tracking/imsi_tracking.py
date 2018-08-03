# Flask
from flask import render_template, redirect, request, url_for, abort, make_response
from flask.views import MethodView

# USCC
from resources.logout import Logout
from uscc_api import api, uscc_eng_app
from resources.imsi import Imsi
from uscc_apps.imsi_tracking.forms import ImsiForm
from common.common import Common

# Misc
import requests
import json
import sys
import os


class ImsiTracking(MethodView):
    def __init__(self):

        self.art = None
        self.imsi_header = {'Authorization': None}
        self.imsi_tracking_dict = dict(imsi=None,
                                       userid=None,
                                       email=None
                                       )
        self.imsi_list_get_resp = None
        self.login_redirect_response = None

    def get(self):
        """
        Receives control from the HTTP GET request when accessing the Imsi tracking web app. Renders the initial html
        web page with the empty web form and does an HTTP GET request to the USCC ENG REST API to retrieve and display
        the current list of tracked imsis.

        :return: Renders the html page with all substituted content needed.
        """

        if request.cookies.get('access_token_cookie') is None:
            self.redirect_to_uscc_login()
            return self.login_redirect_response

        self.imsi_tracking_dict['userid'] = request.cookies.get('username')

        # INFO: needed if JWT_TOKEN_LOCATION is set to headers as opposed to in cookies
        # self.imsi_header['Authorization'] = 'JWT {}'.format(request.cookies.get('access_token_cookie'))
        form = ImsiForm()
        imsi_list = {}
        email_list = {}
        self.imsi_list_get_resp = requests.get(api.url_for(Imsi, _external=True), params=self.imsi_tracking_dict,
                                               headers=self.imsi_header,
                                               cookies={'access_token_cookie': request.cookies.get('access_token_cookie')})
                                               # Uncomment below cookies parameter for JWT token revoke testing.
                                               # Paste existing JWT here and save change (i.e. reload flask app.
                                               # Then use "Logout" button which will register the JWT in the apps
                                               # blacklist. Then login as usual and GET request should fail with a
                                               # "token revoked" type unauthorized response.
                                               # cookies={'access_token_cookie': ''})

        if self.imsi_list_get_resp.status_code == requests.codes.ok:
            if request.args.get('imsi_filter') is not None and request.args.get('imsi_filter') != '':
                imsi_list = self.filter_imsis()
                if len(imsi_list) == 0:
                    imsi_list['0'] = "No Imsi(s) matching filter: '%s'" % request.args.get('imsi_filter')
            else:
                imsi_list = self.imsi_list_get_resp.json().get('imsi_list')

            email_list = self.imsi_list_get_resp.json().get('email_list')
        elif self.imsi_list_get_resp.status_code == requests.codes.unauthorized:
            if self.imsi_list_get_resp.json().get('msg') == 'Token has been revoked':
                self.token_revoked_error()
            else:
                self.redirect_to_uscc_login()
                return self.login_redirect_response
        else:
            get_imsi_list_error = "Retrieving list of tracked Imsi failed with: %s:%s." \
                                  "\nPlease contact Core Automation Team" \
                                  % (str(self.imsi_list_get_resp.status_code), self.imsi_list_get_resp.reason)
            Common.create_flash_message(get_imsi_list_error)

        return render_template('imsi_tracking/imsi_tracking.html', form=form, imsi_list=imsi_list, art=self.art,
                               userid=self.imsi_tracking_dict.get('userid'), email_list=email_list)

    def post(self):
        """
        Receives control after the users clicks submit on the web page via the HTTP POST request done on the HTML form
        action method.

        The string of imsis is extracted from the form and passed on to either a HTTP POST or DELETE request to the
        USCC ENG REST API. Which request to perform is determined by interrogating the Add or Delete radio button to
        determine which value the radio button contains.

        :return: If the form validates correctly then a redirect to the same page is done to reload the page with the
        updated imsi list. If not then the web page is loaded without the imsi list so that any error messages can be
        displayed.
        """

        if 'logout_btn' in request.form:
            self.delete()
            return self.login_redirect_response

        if request.cookies.get('access_token_cookie') is None:
            self.redirect_to_uscc_login()
            return self.login_redirect_response
        else:
            # INFO: needed if JWT_TOKEN_LOCATION is set to headers as opposed to in cookies
            # self.imsi_header['Authorization'] = 'JWT {}'.format(request.cookies.get('access_token_cookie'))
            # INFO: With JWT in cookies set the CSRF token is still expected to be in the header for POST to succeed
            self.imsi_header['X-CSRF-TOKEN'] = request.cookies.get('csrf_access_token')
            self.imsi_header['content_type'] = 'application/json'

        form = ImsiForm()
        if form.validate_on_submit():
            if request.form.get('imsis') == "" and request.form.get('email') == "":
                Common.create_flash_message("Please fill in either the Imsi or Email fields.")
            else:
                self.imsi_tracking_dict['imsi'] = request.form.get('imsis')
                self.imsi_tracking_dict['email'] = request.form.get('email')
                self.imsi_tracking_dict['userid'] = request.cookies.get('username')
                if self.imsi_tracking_dict.get('email') != '' and '@' not in self.imsi_tracking_dict.get('email'):
                    Common.create_flash_message('Email entered is not a valid email address', 'error')
                    return render_template('imsi_tracking/imsi_tracking.html', form=form)
                if request.form['add_delete_radio'] == 'A':
                    imsi_post_resp = \
                        requests.post(api.url_for(Imsi, _external=True), data=json.dumps(self.imsi_tracking_dict),
                                      headers=self.imsi_header,
                                      cookies={'access_token_cookie': request.cookies.get('access_token_cookie')})

                    if imsi_post_resp.status_code == requests.codes.unauthorized:
                        self.redirect_to_uscc_login()
                        return self.login_redirect_response
                    else:
                        if imsi_post_resp.json().get('msg') is not None:
                            Common.create_flash_message("%s. Please Contact Core Automation Team." % imsi_post_resp.json().get('msg'))
                        else:
                            Common.create_flash_message(imsi_post_resp.json().get('imsi_msg'))
                    return redirect(url_for('imsi_tracking'))
                else:
                    self.delete()
                    return redirect(url_for('imsi_tracking'))
        else:
            if len(form.errors) != 0:
                for error_message_text in form.errors.values():
                    Common.create_flash_message(error_message_text[0])

        return render_template('imsi_tracking/imsi_tracking.html', form=form)

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

    def set_art(self):
        """
        Sets the class variable that contains the known JWT access token.
        :return: True if the class instance variable is set otherwise False
        """

        if request.args.get('art') is not None:
            self.art = request.args.get('art')
            self.imsi_header['Authorization'] = 'JWT {}'.format(self.art)
            return True

        return False

    def filter_imsis(self):
        """
        Filters the list of imsi returned from the API to only give those that match the filter value specified by the
        user.

        :return: dictionary of imsis filter by value given in the request args 'imsi_filter' parameter.
        """

        imsi_list = {}
        user_filter = request.args.get('imsi_filter').lower()
        for key, imsi_value in self.imsi_list_get_resp.json().get('imsi_list').items():
            if '(' in imsi_value:
                imsi, alias_right_paren = imsi_value.split('(', 1)
                alias = alias_right_paren.rstrip(')')
                if user_filter.isdigit():
                    if user_filter == imsi:
                        imsi_list[key] = imsi_value
                else:
                    if user_filter == alias.lower():
                        imsi_list[key] = imsi_value
            else:
                if user_filter == imsi_value:
                    imsi_list[key] = imsi_value
        return imsi_list

    def redirect_to_uscc_login(self):
        """
        Redirects to the USCC Login application
        :return: redirect response
        """

        self.login_redirect_response = redirect(os.environ.get('login_app') + '?referrer=' +
                                                url_for('imsi_tracking', _external=True))
        return

    def token_revoked_error(self):
        """
        Scrubs the environment in response to a request to the imsi web app that was made with a revoked token. Which
        includes the following:

            1. Logs the occurrence recording information about the client that made the request and the token used.
            2.  Abort the request with a 401 (unauthorized) response page. Which prevents the browser/client from
                reaching any valid page within the application by just refreshing.

        :return:
        """

        uscc_eng_app.logger.info('Unauthorized access with revoked token attempted. IP=%s: Username=%s: JWT used=%s' %
                                 (request.remote_addr, request.cookies.get('username'),
                                  request.cookies.get('access_token_cookie')))
        abort(401)
