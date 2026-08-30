from odoo import models, fields, api

class HospitalPharmacy(models.Model):
    _name = 'hospital.pharmacy'
    _description = 'Hospital Pharmacy Inventory'
    _rec_name = 'medicine_name'

    medicine_name = fields.Char(string='Medicine Name', required=True)
    category = fields.Char(string='Category')
    stock_qty = fields.Integer(string='Current Stock', default=0)
    reorder_point = fields.Integer(string='Reorder Point', default=50)
    unit_price = fields.Float(string='Unit Price', digits=(16, 2))
    status = fields.Selection([
        ('available', 'Available'),
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out Of Stock')
    ], string='Stock Status', compute='_compute_stock_status', store=True)

    @api.depends('stock_qty', 'reorder_point')
    def _compute_stock_status(self):
        for record in self: 
            if record.stock_qty <= 0:
                record.status = 'out_of_stock'
            elif record.stock_qty <= record.reorder_point:
                record.status = 'low_stock'
            else:
                record.status = 'available'