{
    'name': 'Hospital Management System',
    'version': '16.0.1.0.0',
    'summary': 'A compleate hospital ERP management system for Odoo 16',
    'category': 'Healthcare',
    'author': 'Aronno Chowdhury',
    'depends': ['base', 'board', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/hospital_menu.xml',
        'views/patient_views.xml',
        'views/doctor_views.xml',
        'views/appointment_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}