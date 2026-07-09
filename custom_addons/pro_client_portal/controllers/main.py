from odoo import http
from odoo.http import request


class ProClientPortal(http.Controller):

    @http.route('/my_portal', auth="public", website=True, type="http")
    def my_portal(self, **kw):

        user_id = request.env.user.id

        active_projects_count = request.env['project.project'].sudo().search_count([('user_id', '=', user_id)])
        if active_projects_count > 0:
            project_display_text = f"You have {active_projects_count} active projects."
        else:
            project_display_text = "You have no active project at the moment."
        pending_tasks_count = request.env['project.task'].sudo().search_count([('user_ids', 'in', [user_id]),('stage_id.fold', '=', False)])
        if pending_tasks_count > 0:
            tasks_text = f"You have {pending_tasks_count} pending tasks."
        else:
            tasks_text = "You have no pending tasks at the moment."
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
            'project_text' : project_display_text,
            'pending_tasks' : pending_tasks_count,
            'tasks_text' : tasks_text,
            'total_invoices' : "{:,.2f}".format(float(total_amount)),
            'show_no_invoices' : float(total_amount) == 0.0
        }
        
        return request.render('pro_client_portal.pro_client_portal_page', values)
    
    @http.route('/my_portal/projects', auth="user", website=True, type="http")
    def my_portal_projects(self, **kw):
        user_id = request.env.user.id
        projects = request.env['project.project'].sudo().search([('user_id', '=', user_id)])
        values = {
            'projects': projects,
        }
        return request.render('pro_client_portal.pro_client_portal_projects_page', values)
    
    @http.route('/my_portal/tasks', auth="user", website=True, type="http")
    def my_portal_tasks(self, **kw):
        user_id = request.env.user.id
        tasks = request.env['project.task'].sudo().search([('user_ids', 'in', [user_id]), ('stage_id.fold', '=', False)])
        values = {
            'tasks' : tasks,
        }
        return request.render('pro_client_portal.pro_client_portal_tasks_page', values)
    
    @http.route('/my_portal/invoices', auth="user", website=True, type="http")
    def my_portal_invoices(self, **kw):
        partner_id = request.env.user.partner_id.id
        invoices = request.env['account.move'].sudo().search([('move_type', '=', 'out_invoice'), ('state', '=', 'posted'), ('partner_id', '=', partner_id)])
        values = {
            'invoices' : invoices,
        }
        return request.render('pro_client_portal.pro_client_portal_invoices_page', values)