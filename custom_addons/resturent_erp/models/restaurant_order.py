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

    date_order = fields.Datetime(string='Order Date', default=fields.Datetime.now, tracking=True)

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


    @api.model
    def _get_dashboard_matrics(self):
        today = fields.Date.today()
        domain = [('date_order', '>=', f'{today} 00:00:00'), ('date_order', '<=', f'{today} 23:59:59'), ('state', '=', 'compleated')]

        today_orders = self.search(domain)
        today_revenue = sum(today_order.mapped('amount_total'))

        total_tables = self.env['resturent.table'].search_count([])
        occupied_tables = self.env['restaurant.order'].search_count([('state', 'in', ['draft', 'preparing', 'ready'])])

        occupancy_rate = 0
        if total_tables > 0:
            occupancy_rate = int((occupied_tables / total_tables) * 100)

        return {
            'today_revenue': today_revenue,
            'occupancy_rate': occupancy_rate,
            'occupied_tables': occupied_tables
        }

class RestaurantOrderLine(models.Model):
    _name = "restaurant.order.line"
    _description = "Restaurant Order Line"

    order_id = fields.Many2one('restaurant.order', string='Order Reference', required=True, ondelete='cascade')
    menu_item_id = fields.Many2one('restaurant.menu.item', string='Food Item', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Price Unit', required=True)
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_price_subtotal', store=True)

    @api.onchange('menu_item_id')
    def _onchange_menu_item_id(self):
        if self.menu_item_id:
            self.price_unit = self.menu_item_id.price

    @api.depends('quantity', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price_unit
            