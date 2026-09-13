from odoo import models, fields, api
from odoo.exceptions import UserError

class PatientReportWizard(models.TransientModel):
    _name = 'patient.report.wizard'
    _description = 'Patient Report Wizard'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    status = fields.Selection([
        ('all', 'All Patients'),
        ('inpatient', 'Inpatient'),
        ('outpatient', 'Outpatient'),
        ('discharged', 'Discharged')
    ], string='Status Filter', default='all')

    def action_print_report(self):
        domain = []
        if self.patient_id:
            domain.append(('id', '=', self.patient_id.id))
        elif self.status and self.status != 'all':
            domain.append(('status', '=', self.status))

        patients = self.env['hospital.patient'].search(domain)
        if not patients:
            raise UserError("No patient records found matching the selected criteria.")

        return self.env.ref('hospital_management.action_report_patient_card').report_action(patients)
