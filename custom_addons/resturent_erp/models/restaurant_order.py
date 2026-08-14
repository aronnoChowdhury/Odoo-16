from odoo import models, fields, api

class RestaurantOrder(models.Model):
    _name = "restaurant.order"
    _description = "Restaurant Order Management"
    _order = "id desc"

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default=lambda self: 'New')
    table_id = fields.Many2one('resturent.table', string='Table', required=True)
    customer_name = fields.Char(string='Customer Name')
    order_line_ids = fields.One2many('restaurant.order.line', 'order_id', string='Order Line')
    amount_total = fields.Float(string='Total Amount', compute='_compute_amount_total', store=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'), 
        ('compleated', 'Compleated'), 
        ('cancelled', 'Cancelled')
    ])

    payment_state = fields.Selection([
        ('not_paid', 'Not Paid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid')
    ], string='Payment Status', default='not_paid', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('restaurant.order') or 'New'
        return super(RestaurantOrder, self).create(vals)

    @api.depends('order_line_ids.price_subtotal')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(line.price_subtotal for line in order.order_line_ids)

    def action_mark_as_ready(self):
        for order in self:
            order.state = 'ready'

    def action_mark_as_completed(self):
        for order in self:
            order.state = 'compleated'

    def action_confirm_payment(self):
        for order in self:
            if order.state != 'compleated':
                raise UserError("Only compleated orders can be paid.")
            order.payment_state = 'paid'


class RestaurantOrderLine(models.Model):
    _name = "restaurant.order.line"
    _description = "Restaurant Order Line"

    order_id = fields.Many2one('restaurant.order', string='Order Reference', required=True, ondelete='cascade')
    menu_item_id = fields.Many2one('restaurant.menu.item', string='Food Item', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Price Unit', required=True)
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_price_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price_unit
            