from odoo import models, fields, api

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient Management'
    _rec_name = 'full_name'

    patient_id = fields.Char(string='Patient ID', required=True, copy=False, readonly=True, default='New')
    full_name = fields.Char(string='Full Name', required=True)
    contact_number = fields.Char(string='Contact Number', required=True)
    last_visit_date = fields.Date(string='Last Visit Date', default=fields.Date.today)
    next_appointment= fields.Date(string='Next Appointment')
    status = fields.Selection([
        ('inpatient', 'Inpatient'),
        ('outpatient', 'Outpatient'),
        ('discharged', 'Discharged')
    ], string='Patient Status', default='outpatient')


    @api.model
    def create(self, vals):

        if vals.get('patient_id', 'New') == 'New':
            vals['patient_id'] = self.env['ir.sequence'].next_by_code(
                'hospital.patient'
            ) or 'New'

        return super(HospitalPatient, self).create(vals)

