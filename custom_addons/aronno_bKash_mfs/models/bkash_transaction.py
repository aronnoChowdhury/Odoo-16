from odoo import models, fields, api

class BkashTransaction(models.Model):
    _name = 'bkash.transaction'
    _description = 'bKash Trnasaction'

    recipient = fields.Char(string='Recipient/Agent Number', required=True)
    amount = fields.Float(string='Amount', required=True)
    tnx_type = fields.Selection([
        ('send_money', 'Send Money'),
        ('cash_out', 'Cash Out'),
        ('recharge', 'Recharge')
    ], string='Transaction Type', required=True)
    operator = fields.Char(string='Operator')
    tnx_id = fields.Char(string='Transaction ID', required=True)
    user_id = fields.Many2one('res.users', string = 'User', default = lambda self: self.env.user, required=True)