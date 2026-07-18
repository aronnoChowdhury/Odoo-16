{
    'name' : 'Advanced Sales Customization',
    'version' : '1.0',
    'author' : 'Aronno Chowdhury',
    'category' : 'Sales',
    'summary' : 'Advanced Sales Comunication and Custom Dashboard',
    'description': """
    Advanced Sales Customization Module.

    Features:
    - Sales Order Customization
    - Commission Calculation
    - Commission PDF Report
    - Custom Dashboard
    - Custom Backend Styling (SCSS)
    """,
    'depends' : ['sale_management', 'web',],
    'data' : [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sales_order_views.xml',
        'views/sales_order_report.xml'
    ],
    'assets' : {
        'web.assets_backend' : [
            'sales_customization/static/src/scss/custom_style.scss',
        ]
    },
    'application' : False,
    'installable' : True,
}