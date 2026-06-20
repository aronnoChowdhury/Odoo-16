from odoo import http
from odoo.http import request


class ProClientPortal(http.Controller):

    @http.route('/my_portal', auth="public", website=True, type="http")
    def my_portal(self, **kw):

        user_id = request.env.user.id

        active_projects_count = request.env['project.project'].sudo().search_count([('user_id', '=', user_id)])
        pending_tasks_count = request.env['project.task'].sudo().search_count([('user_ids', 'in', [user_id]),('stage_id.fold', '=', False)])
        total_invoices_amount = request.env['account.move'].sudo().read_group(
            [('move_type', '=', 'out_invoice'),('state', '=', 'posted'),('partner_id', '=', request.env.user.partner_id.id)],
            ['amount_total'], 
            []
            )
        if total_invoices_amount and total_invoices_amount[0].get('amount_total') is not None:
            total_amount = total_invoices_amount[0]['amount_total']
        else:
            total_amount = 0.0

        values ={

            'message' : 'Welcome to the Pro Client Portal! Here you can access your information, communicate with us, and manage your interactions securely and efficiently.',
            'active_projects' : active_projects_count,
            'pending_tasks' : pending_tasks_count,
            'total_invoices' : "{:,.2f}".format(float(total_amount))
        }
        
        return request.render('pro_client_portal.pro_client_portal_page', values)