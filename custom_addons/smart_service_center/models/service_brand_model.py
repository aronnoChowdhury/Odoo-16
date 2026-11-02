from odoo import models, fields, api 

class ServiceDeviceBrand(models.Model): 
    _name = 'service.device.brand' 
    _description = 'Service Device Brand' 
    _order = 'name asc' 

    name = fields.Char(string='Brand Name', required=True, translate=True) 
    code = fields.Char(string='Brand Code', help='Short code e.g. APL, SAM, HP') 
    logo = fields.Binary(string='Brand Logo') 
    active = fields.Boolean(default=True) 
    model_ids = fields.One2many(
        'service.device.model', 
        'brand_id', 
        string='Device Models'
    )
    model_count = fields.Integer(string='Model Count', compute='_compute_model_count', store=True) 

    @api.depends('model_ids') 
    def _compute_model_count(self): 
        for brand in self: 
            brand.model_count = len(brand.model_ids) 

class ServiceDeviceModel(models.Model): 
    _name = 'service.device.model' 
    _description = 'Service Device Model' 
    _order = 'name asc' 

    name =  fields.Char(string='Model Name', required=True) 
    brand_id = fields.Many2one( 
        'service.device.brand', 
        string='Brand', required=True, ondelete='cascade'
    )
    device_type = fields.Selection([
        ('mobile', 'Mobile / Smartphone'), 
        ('laptop', 'Laptop / PC'), 
        ('Tablet', 'Tablet / ipad'), 
        ('appliance', 'Home Appliance'), 
        ('other', 'Other Devices')
    ], string='Device Category', default='mobile', required=True) 
    default_warranty_months = fields.Integer(string='Default Warranty (Months)', default=12, help='Standard manufacturer warranty period in months') 
    notes = fields.Text(string='Technical Specs / Notes')  

class ServiceDefectType(models.Model): 
    _name = 'service.defect.type' 
    _description = 'Service Defect / Problem Type' 
    _order = 'sequence, name' 

    sequence  = fields.Integer(default=10) 
    name = fields.Char(string='Dedect / Issue Name', required=True) 
    code = fields.Char(string='Defect Code') 
    description = fields.Text(string='Description / Common Symptoms')