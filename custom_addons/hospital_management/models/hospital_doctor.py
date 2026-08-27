from odoo import models, fields

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor Management'
    _rec_name = 'name'

    name = fields.Char(string='Doctor Name', required=True)
    specialization = fields.Char(string='Specialization')
    phone = fields.Char(string='Phone')
    available_time = fields.Char(string='Available Time', default='9:00 AM - 5:00 PM')
