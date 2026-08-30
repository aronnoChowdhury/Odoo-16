from odoo import models, fields

class HospitalLab(models.Model):
    _name = 'hospital.lab'
    _description = 'Hospital Leboratory Tests'
    _rec_name = 'test_name'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    test_name = fields.Char(string='Test Name', required=True)
    test_date = fields.Datetime(string='Test Date', default=fields.Datetime.now)
    result_summary = fields.Text(string='Result Summary')
    state = fields.Selection([
        ('pending', 'Pending'), 
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], string='Status', default='pending')