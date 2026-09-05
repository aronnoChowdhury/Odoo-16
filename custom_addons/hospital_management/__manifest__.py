{
    'name': 'Hospital Management System',
    'version': '16.0.1.0.0',
    'summary': 'A complete hospital ERP management system for Odoo 16',
    'category': 'Healthcare',
    'author': 'Aronno Chowdhury',
    'depends': ['base', 'board', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/patient_views.xml',
        'views/doctor_views.xml',
        'views/appointment_views.xml',
        'views/hospital_pharmacy.xml',
        'views/lab_views.xml',
        'views/hospital_accounting.xml',
        'views/hospital_report.xml',
        'views/hospital_dashboard.xml',
        'views/hospital_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hospital_management/static/src/scss/hospital_management.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
