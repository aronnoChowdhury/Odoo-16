from odoo import http
from odoo.http import request


class BkashFrontendController(http.Controller):

    @http.route(['/bkash'], type='http', auth='user', website=True)
    def bkash_dashboard(self, **kwargs):
        return request.render('aronno_bKash_mfs.bkash_dashboard_template', {})