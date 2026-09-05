from odoo import http
from odoo.http import request

class HospitalWebsite(http.Controller):

    @http.route('/hospital/appointments', type="http", auth="public", website=True)
    def hospital_appointments(self, *kw):
        doctors = request.env['hospital.doctor'].sudo().search([])
        return request.render('hospital_management.hospital_appointments', {'doctors': doctors})


    @http.route('/hospital/appointment/submit', type="http", auth="public", methods=['POST'], website=True, csrf=False)
    def hospital_appointment_submit(self,**post):

        request.env['hospital.appointment'].sudo().create({
            'patient_id': post.get('patient_name'),
            'doctor_id': int(post.get('doctor_id')),
            'appointment_date': post.get('appointment_date'),
        })

        return request.render('hospital_management.hospital_appointment_thankyou', {})
