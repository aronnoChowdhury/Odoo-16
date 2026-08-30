from odoo import models, fields, api

class HospitalAccounting(models.Model):
    _name = 'hospital.accounting'
    _description = 'Hospital Patient Accounting'
    _rec_name = 'name'

    name = fields.Char(string='Hospital Accounting', required=True, copy=False, readonly=True, default=lambda self:'New')
    patient_id = fields.Many2one('hospital.patient', string='patient', required=True)
    doctor_fee = fields.Float(string='Doctor Fee', default=0.0)
    medicine_fee = fields.Float(string='Medicine Fee', default=0.0)
    lab_fee = fields.Float(string='Lab Test Fee', default=0.0)
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')

    @api.depends('doctor_fee', 'medicine_fee', 'lab_fee')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.doctor_fee + rec.medicine_fee + rec.lab_fee 

    @api.model
    def create(self, vals):
        if vals.get('name', 'New')  == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.accounting')
        return super(HospitalAccounting, self).create(vals)
