from odoo import models, fields, api

class HospitalReport(models.Model):
    _name = 'hospital.report'
    _description = 'Hospital Management Reports'
    _auto = False

    name = fields.Char(string='Report Name')
    total_patients = fields.Integer(string='Total Patients')
    total_appointments = fields.Integer(string='Total Appointments')
    total_revenue = fields.Float(string='Total Revenue')

    def init(self):
        pass 

