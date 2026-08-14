from odoo import models, fields, api

class RestaurantKitchenKDS(models.Model):
    _name = "restaurant.kitchen.kds"
    _description = "Restaurant Kitchen Display System"
    _order = "priority desc, id desc"

    order_id = fields.Many2one("restaurant.order", string="Order Reference", required=True, ondelete="cascade")
    table_id = fields.Many2one("resturent.table", string="Table", related='order_id.table_id', store=True)
    order_line_ids = fields.One2many("restaurant.order.line", related='order_id.order_line_ids', string="Order Lines")

    state = fields.Selection([
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered')
    ], string='Kitchen Status', default='preparing', tracking=True)

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Urgent')
    ], string='Priority', default='0')

    def action_mark_ready(self):
        for record in self:
            record.state = 'ready'
            if record.order_id:
                record.order_id.state = 'ready'