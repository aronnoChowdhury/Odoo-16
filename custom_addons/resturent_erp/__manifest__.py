{
    'name': 'Restaurant ERP & Management',
    'version': '16.0.1.0.0',
    'category': 'Industry',
    'summary': 'Professional Resturent ERP with POS, KDS, and Table Management',
    'author': 'Aronno Chowdhury',
    'depends': ['base', 'web'],
    'data':[
        'security/ir.model.access.csv',
        'views/table_view.xml',
        'views/order_view.xml',
    ],
    'assets': {
        'web.assets_backend':[
            'resturent_erp/static/src/scss/restaurant_style.scss',
        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}