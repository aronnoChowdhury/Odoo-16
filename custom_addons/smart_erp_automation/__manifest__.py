{
    'name': 'Smart ERP AI - Sales, Purchase, Inventory & Accounting Automation',
    'version': '16.0.1.0.0',
    'author': 'Aronno Chowdhury',
    'depends': ['base', 'sale_management', 'purchase', 'stock', 'account', 'mail'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': True,
}