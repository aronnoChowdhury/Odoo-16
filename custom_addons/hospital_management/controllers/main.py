from odoo import http 
from odoo.http import request

class HospitalWebsite(http.Controller):

    @http.route('/hospital/appointments', type='http', auth='public', website=True)
    def hospital_appointments(self, *kw):
        doctors = request.env['hospital.doctor'].sudo().search([])

        return request.render('hospital_management.hospital_appointment_web_form', {'doctors': doctors})

    @http.route('/hospital/appointment/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def hospital_appointment_submit(self, **post):
        patient_name = post.get('patient_name')
        doctor_id = post.get('doctor_id')
        appointment_date = post.get('appointment_date')

        patient = request.env['hospital.patient'].sudo().search([
            ('full_name', '=', patient_name),
        ],limit=1)


        if patient: 
            if appointment_date:
                appointment_date = appointment_date.replace('T', ' ')

            request.env['hospital.appointment'].sudo().create({
                'patient_id': patient.id, 
                'doctor_id': int(doctor_id), 
                'appointment_date': appointment_date,
            })

            return request.render('hospital_management.hospital_appointment_thankyou', {})

        doctors = request.env['hospital.doctor'].sudo().search([])

        return request.render('hospital_management.hospital_appointment_web_form', {
            'doctors': doctors,
            'error': 'Patient not found. Please register as a patient first.'
        })