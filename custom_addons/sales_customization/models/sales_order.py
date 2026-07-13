from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    commission_total = fields.Float(string='Total Commission', compute='_compute_commission', store=True)

    @api.depends('order_line.price_subtotal', 'order_line.product_id')
    def _compute_commission(self):
        for order in self:
            total_comm = 0.0
            for line in order.order_line:
                if line.product_id.categ_id.name == 'All / Saleable':
                    total_comm += line.price_subtotal * 0.10
                else:
                    total_comm += line.price_subtotal * 0.05
            order.commission_total = total_comm