from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_limit_amount = fields.Monetary(
        string= "Credit Limit",
        currency_field = 'currency_id', default= 50000.0, help= "Maximum allowed credit for this customer before orders require manager approval."
    )

    total_due_amount = fields.Monetary(
        string="Total Open Due",
        currency_field='currency_id',
        compute = '_compute_partner_financial_metrics', 
        store=True, help="Sum of unpaid and overdue invoices."
    )

    credit_risk_level = fields.Selection([
        ('low', 'Low Risk (Good Standing)'),
        ('medium', 'Medium Risk (Moderate Usage)'), 
        ('high', 'High Risk (Near Limit)'), 
        ('critical', 'Critical Risk (Exceeded Limit)')
    ], string="Credit Risk Level", compute='_compute_partner_financial_metrics', store=True)


    @api.depends('invoice_ids', 'invoice_ids.state', 'invoice_ids.payment_state', 'credit_limit_amount') 

    def _compute_partner_financial_metrics(self):
        for partner in self:
            open_invoices = partner.invoice_ids.filtered(
                lambda inv: inv.move_type == 'out_invoice' and inv.state == 'posted' and inv.payment_state in ('not_paid', 'partial')
            )
            total_due = sum(open_invoices.mapped('amount_residual'))
            partner.total_due_amount = total_due 

            limit = partner.credit_limit_amount or 1.0
            ratio = (total_due / limit) * 100.0 if limit > 0 else 0.0 

            if total_due > limit: 
                partner.credit_risk_level = 'critical'
            elif ratio >= 80.0:
                partner.credit_risk_level = 'high'
            elif ratio >= 40.0: 
                partner.credit_risk_level = 'medium'
            else: 
                partner.credit_risk_level = 'low'