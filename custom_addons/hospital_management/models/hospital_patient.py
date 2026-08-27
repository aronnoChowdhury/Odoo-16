from odoo import models, fields

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient Management'
    _rec_name = 'full_name'

    patient_id = fields.Char(string='Patient ID', required=True, copy=False, readonly=True, default=lambda self: '3001')
    full_name = fields.Char(string='Full Name', required=True)
    contact_number = fields.Char(string='Contact Number', required=True)
    last_visit_date = fields.Date(string='Last Visit Date', default=fields.Date.today)
    next_appointment= fields.Date(string='Next Appointment')
    status = fields.Selection([
        ('inpatient', 'Inpatient'),
        ('outpatient', 'Outpatient'),
        ('discharged', 'Discharged')
    ], string='Patient Status', default='outpatient')

