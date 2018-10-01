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
from openerp.addons.website_tansaction_create_account.controllers.main import my_website_sale_auth

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


class AccountSignUpDetails(my_website_sale_auth):

    @http.route()
    def sale_auth(self, redirect=None, *args, **kw):
        res = super(AccountSignUpDetails, self).sale_auth(redirect=redirect, *args, **kw)
        res.qcontext.update({
            'states': request.env["res.country.state"].sudo().search([]),
            'countries': request.env["res.country"].sudo().search([]),
        })

        return res


class AccountSignUpDetailsExt(website_sale):

    def get_auth_signup_qcontext(self):
        """ Shared helper returning the rendering
        context for signup and reset password """
        qcontext = request.params.copy()
        qcontext['states'] = request.env["res.country.state"].sudo().search([])
        qcontext['countries'] = request.env["res.country"].sudo().search([])
        return qcontext
