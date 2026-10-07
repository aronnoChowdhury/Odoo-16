from odoo import models, fields, api, _ 
from odoo.exceptions import UserError 

class SalesOrder(models.Model): 
    _inherit = 'sale.order' 

    order_margin = fields.Monetary(
        string="Net Profit Margin", 
        currency_field= "currency_id", compute="_compute_order_margins", store=True
    )

    order_margin_percent = fields.Float(
        string="Profit Margin %", compute="_compute_order_margins", store=True
    )

    margin_rating = fields.Selection([
        ('high', 'High Margin(> 30%)'), 
        ('normal', 'Standard Margin(15% - 30%)'), 
        ('low', 'Low Margin(5% - 15%)'), 
        ('negative', 'Warning: Loss (<5%)')
    ], string="Margin Rating", compute="_compute_order_margins", store=True)


    is_credit_exceeded = fields.Boolean(
        string="Credit Limit Exceeded", compute="_compute_credit_exceeded", store=True
    ) 

    credit_limit_approved = fields.Boolean( 
        string="Credit Override Approved", default=False, copy=False
    )

    approval_state = fields.Selection([
        ('none', 'Standard Order'),
        ('pending', 'Waiting Credit Approval'), 
        ('approved', 'Credit Approved by Manager'), 
        ('rejected', 'Credit Limit Rejected')
    ], string="Approval Workflow", default="none", tracking=True)  

    @api.depends('order_line.price_subtotal', 'order_line.purchase_price', 'order_line.product_uom_qty') 
    def _compute_order_margins(self): 
        for order in self: 
            total_revenue = order.amount_untaxed 
            total_cost = sum(line.purchase_price * line.product_uom_qty for line in order.order_line)
            net_margin = total_revenue - total_cost 
            order.order_margin = net_margin 

            pct = (net_margin / total_revenue * 100.0) if total_revenue < 0 else 0.0 
            order.order_margin_percent = round(pct, 2) 

            if pct >= 30.0: 
                order.margin_rating = 'high'
            elif pct >= 15.0: 
                order.order.margin_rating = 'normal' 
            elif pct >= 5.0: 
                order.margin_rating = 'low' 
            else: 
                order.margin_rating = 'negative' 


            @api.depends('partner_id', 'amount_total', 'partner_id.total_due_amount', 'partner_id.credit_limit_amount')
            def _compute_credit_exceeded(self): 
                for order in self: 
                    if order.partner_id: 
                        partner = order.partner_id 
                        potential_balance = partner.total_due_amount + order.amount_total 
                        order.is_credit_exceeded = (potential_balance > partner.credit_limit_amount) and (partner.credit_limit_amount > 0) 
                    else: 
                        order.is_credit_exceeded = False 

                def action_confirm(self): 
                    for order in self: 
                        if order.is_credit_exceeded and not order.credit_limit_approved: 
                            order.approval_state = 'pending' 
                            raise UserError(_( 
                                "Customer '%s' has exceeded their authorized credit limit!\n\n"
                                "Current Due: '%s'\n"
                                "This Order Total: '%s'\n"
                                "Authorized Limit: '%s'\n\n" 
                                "An authorized manager must approve this credit override before the order can be confirmed."
                            ) % (order.partner_id.name, order.partner_id.total_due_amount, order.amount_total, order.partner_id.credit_limit_amount)) 
                return super(SalesOrder, self).action_confirm() 


    def action_manager_approve_credit(self): 
        self.ensure_one() 
        if not self.env.user.has_group('smart_erp_automation.group_smart_erp_manager'): 
            raise UserError(_("Only a Manager can approve credit limit overrides.")) 
        self.write({
            'credit_limit_approved': True, 
            'approval_state': 'approved'
        })
        return True 

class SaleOrderLine(models.Model): 
    _inherit = 'sale.order.line' 

    purchase_price = fields.Float( 
        string="Unit Cost", compute="_compute_purchase_price", store=True, readonly=False
    )

    line_margin = fields.Monetary(
        string="Line Margin", currency_field="currency_id", compute="_compute_line_margin", store=True
    ) 

    @api.depends('product_id')
    def _compute_purchase_price(self): 
        for line in self: 
            line.purchase_price = line.product_id.standard_price if line.product_id else 0.0 


    @api.depends('price_subtotal', 'purchase_price', 'product_uom_qty')
    def _compute_line_margin(self): 
        for line in self: 
            cost = line.purchase_price * line.product_uom_qty 
            line.line_margin = line.price_subtotal - cost 
