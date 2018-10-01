# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################

import logging
import werkzeug
import openerp
from openerp.addons.auth_signup.res_users import SignupError
from openerp.addons.web.controllers.main import ensure_db
from openerp import http
from openerp.http import request
from openerp.addons.website_sale.controllers.main import website_sale

_logger = logging.getLogger(__name__)

def login_redirect_a():
    url = '/sale_login?'
    # built the redirect url, keeping all the query parameters of the url
    redirect_url = '%s?%s' % (
        request.httprequest.base_url, werkzeug.urls.url_encode(request.params))
    return """<html><head><script>
    window.location = '%sredirect=' + encodeURIComponent("%s" + location.hash);
    </script></head></html>
    """ % (url, redirect_url)

class AccountSignUpDetails(website_sale):
    @http.route(['/sale_login'], type='http', auth="public", website=True)
    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = dict((key, qcontext.get(key))
                      for key in ('login', 'name', 'password', 'state_id', 'country_id'))
        assert any([k for k in values.values()]
                   ), "The form was not properly filled in."
        assert values.get('password') == qcontext.get(
            'confirm_password'), "Passwords do not match; please retype them."
        values['lang'] = request.lang
        self._signup_with_values(qcontext.get('token'), values)
        request.cr.commit()

class AccountSignUpDetailsExt(website_sale):

    def get_auth_signup_qcontext(self):
        """ Shared helper returning the rendering
        context for signup and reset password """
        qcontext = request.params.copy()
        qcontext['states'] = request.env["res.country.state"].sudo().search([])
	qcontext['countries'] = request.env["res.country"].sudo().search([])
        return qcontext
