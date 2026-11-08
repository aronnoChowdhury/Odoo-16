from odoo import models, fields, api, _ 
from odoo.exceptions import UserError, ValidationError 

class ServiceOrder(models.Model): 
    _name = 'service.order' 
    _description = 'Service Order / Job Sheet' 
    _inherit = ['mail.thread', 'mail.activity.mixin'] 
    _order = 'id desc' 

    name = fields.Char(string='Job Sheet No', required=True, copy=False, readonly=True, default=lambda self: _('New'), tracking=True) 
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True) 
    partner_phone = fields.Char(string='Phone', related='partner_id.phone', readonly=False) 
    partner_email = fields.Char(string='Email', related='partner_id.email', readonly=False) 

    brand_id = fields.Many2one('service.device.brand', string='Device Brand', required=True, tracking=True) 

    model_id = fields.Many2one('service.device.model', string='Device Model', required=True, tracking=True, domain="[('brand_id', '=', brand_id)]") 
    serial_no = fields.Char(string='Serial No / IMEI', tracking=True) 
    warranty_type = fields.Selection([
        ('in_warranty', 'In Warranty (Free Service)'), 
        ('out_warranty', 'Out of Warranty (Paid Service)'), 
        ('amc', 'AMC Contract'),
    ], string='Warranty Status', default='out_warranty', required=True, tracking=True)  

    defect_type_ids = fields.Many2many('service.defect.type', string='Reported Defects / Issues') 
    customer_problem = fields.Text(string='Customer Complaint / Symptoms', required=True) 
    technical_notes = fields.Text(string='Technician Diagnosis & Action Taken') 

    technician_id = fields.Many2one('res.users', string='Assigned Technician', default=lambda self: self.env.user, tracking=True) 
    date_received = fields.Datetime(string='Received Date', default=fields.Datetime.now, readonly=True) 
    date_deadline = fields.Date(string='Target Delivery Date', tracking=True) 
    priority = fields.Selection([
        ('0', 'Low'), 
        ('1', 'Normal'), 
        ('2', 'High'), 
        ('3', 'Urgent')
    ], string='Priority', default='1') 

    state = fields.Selection([
        ('draft', 'Draft / Intake'), 
        ('diagnosing', 'Under Diagnosis'), 
        ('quotation', 'Quotation / Estimation'), 
        ('in_progress', 'Repair In Progress'), 
        ('qc', 'Quality Control (QC)'), 
        ('ready', 'Ready for Delivery'), 
        ('delivered', 'Delivered & Closed'), 
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, copy=False) 

    order_line_ids = fields.One2many('service.order.line', 'order_id', string='Parts & Labor Lines') 

    amount_parts = fields.Monetary(string='Parts Total', compute='_compute_amounts', store=True, currency_field='currency_id') 
    amount_labor = fields.Monetary(string='Labor Total', compute='_compute_amounts', store=True, currency_field='currency_id') 
    amount_total = fields.Monetary(string='Grand Total', compute='_compute_amounts', store=True, currency_field='currency_id') 
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id) 

    @api.depends('order_line_ids.price_subtotal', 'order_line_ids.type') 
    def _compute_amounts(self): 
        for order in self: 
            parts = 0.0 
            labor = 0.0 
            for line in order.order_line_ids: 
                if line.type == 'part': 
                    parts += line.price_subtotal 
                elif line.type == 'service': 
                    labor += line.price_subtotal 
            order.amount_parts = parts 
            order.amount_labor = labor 
            order.amount_total = parts + labor 


    @api.onchange('brand_id') 
    def _onchange_brand_id(self): 
        if self.brand_id and self.model_id and self.model_id.brand_id != self.brand_id: 
            self.model_id = False 


    @api.model
    def create(self, vals): 
        if vals.get('name', _('New')) == _('New'): 
            vals['name'] = self.env['ir.sequence'].next_by_code('service.order') or _('New') 
        return super(ServiceOrder, self).create(vals)  


    def action_start_diagnosis(self): 
        self.write({'state': 'diagnosing'}) 

    def action_create_quotation(self): 
        self.write({'state': 'quotation'}) 

    def action_start_repair(self): 
        self.write({'state': 'in_progress'}) 

    def action_start_qc(self): 
        self.write({'state': 'qc'}) 

    def action_ready_for_delivery(self): 
        self.write({'state': 'ready'})  

    def action_deliver(self): 
        self.write({'state': 'delivered'})  

    def action_cancel(self): 
        self.write({'state': 'cancelled'})  

    def action_reset_draft(self): 
        self.write({'state': 'draft'})  


class ServiceOrderLine(models.Model): 
    _name = 'service.order.line'
    _description = 'Service Order Line (Parts & Services)' 

    order_id  = fields.Many2one('service.order', string='Service Order', ondelete='cascade', required=True) 
    product_id = fields.Many2one('product.product', string='Product / Service', required=True) 
    name = fields.Text(string='Description', required=True) 
    type = fields.Selection([
        ('part', 'Spare Part'), 
        ('service', 'Service / Labor Charge'),
    ], string='Line Type', default='part', required=True) 

    product_uom_qty = fields.Float(string='Quantity', default=1.0) 
    price_unit = fields.Float(string='Unit Price', default=0.0) 
    is_warranty = fields.Boolean(string='Covered Under Warrenty', help='If checked, customer id not charged for this part') 

    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_subtotal', store=True, currency_field='currency_id') 
    currency_id = fields.Many2one(related='order_id.currency_id', string='Currency', readonly=True) 


    @api.onchange('product_id') 
    def _onchange_product_id(self): 
        if self.product_id: 
            self.name = self.product_id.display_name 
            self.price_unit = self.product_id.list_price 

            if self.product_id.type == 'service': 
                self.type = 'service' 
            else: 
                self.type = 'part' 

    @api.depends('product_uom_qty', 'price_unit', 'is_warranty') 
    def _compute_subtotal(self): 
        for line in self: 
            if line.is_warranty: 
                line.price_subtotal = 0.0 
            else: 
                line.price_subtotal = line.product_uom_qty * line.price_unit 
                
    
        