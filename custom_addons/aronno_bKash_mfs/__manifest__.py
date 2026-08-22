{
    'name': 'Aronno bKash MFS Simulation',
    'version': '16.0.1.0.0',
    'summary': 'A custom Mobile Financial Service web module inspired by bKash build for Odoo 16.',
    'description': """
        A custom Odoo 16 module featuring a mobile financial service (bKash style) 
        frontend interface, user accounts, and transaction management.
    """,
    'category': 'Website/Finance',
    'author': 'Aronno Chowdhury',
    'depends': ['base', 'website'],
    'data': [
        'views/bKash_templates.xml',
        'views/bkash_header.xml',
        'views/bkash_footer.xml',
        'views/template.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}