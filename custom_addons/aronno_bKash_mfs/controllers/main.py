import random
import string
from odoo import http
from odoo.http import request


class BkashFrontendController(http.Controller):

    @http.route(['/bkash', '/bkash/home'], type='http', auth='user', website=True)
    def bkash_dashboard(self, **kwargs):
        return request.render('aronno_bKash_mfs.bkash_dashboard_template', {})

    @http.route(['/bkash/history'], type='http', auth='user', website=True)
    def bkash_history(self, **kwargs):
        return request.render('aronno_bKash_mfs.bkash_history_template', {})

    @http.route(['/bkash/settings'], type='http', auth='user', website=True)
    def bkash_settings(self, **kwargs):
        return request.render('aronno_bKash_mfs.bkash_settings_template', {})

    @http.route(['/bkash/profile'], type='http', auth='user', website=True)
    def bkash_profile(self, **kwargs):
        return request.render('aronno_bKash_mfs.bkash_profile_template', {})

    @http.route(['/bkash/send-money'], type='http', auth="user", website=True)
    def bkash_send_money(self, **kwargs):
        return request.render('aronno_bKash_mfs.bkash_send_money_template', {})

    @http.route(['/bkash/cash-out'], type='http', auth='user', website=True)
    def bkash_cash_out(self, **kwargs):
        return request.render('aronno_bKash_mfs.bkash_cash_out_template', {})

    @http.route(['/bkash/recharge'], type='http', auth='user', website=True)
    def bkash_recharge(self, **kwargs):
        return request.render('aronno_bKash_mfs.bkash_recharge_template', {})

    @http.route('/bkash/send-money/submit', type='http', auth='user', methods=['POST'], website=True)
    def bkash_send_money_submit(self, **post):
        recipient = post.get('recipient_number')
        amount = post.get('amount')
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return request.render('aronno_bKash_mfs.bkash_success_template', {
            'action': 'Send Money',
            'recipient': recipient,
            'amount': amount,
            'random_suffix': random_suffix,
        })

    @http.route('/bkash/cash-out/submit', type='http', auth='user', methods=['POST'], website=True)
    def bkash_cash_out_submit(self, **post):
        agent = post.get('agent_number')
        amount = post.get('amount')
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return request.render('aronno_bKash_mfs.bkash_success_template', {
            'action': 'Cash Out',
            'recipient': agent,
            'amount': amount,
            'random_suffix': random_suffix,
        })

    @http.route('/bkash/recharge/submit', type='http', auth='user', methods=['POST'], website=True)
    def bkash_recharge_submit(self, **post):
        recipient = post.get('recipient_number')
        operator = post.get('operator')
        amount = post.get('amount')
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return request.render('aronno_bKash_mfs.bkash_success_template', {
            'action': 'Mobile Recharge',
            'recipient': recipient,
            'operator': operator,
            'amount': amount,
            'random_suffix': random_suffix,
        })


    