from odoo import models, fields

class ResturentTable(models.Model):
    _name = 'resturent.table'
    _description = 'Restaurant Table Management'

    name = fields.Char(string='Table Name/Number', required=True)
    capacity = fields.Integer(string='Seating Capacity', default=4)
    status = fields.Selection([
        ('free', 'Free'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved')
    ], string='Status', default='free', required=True)
    notes = fields.Text(string='Notes')