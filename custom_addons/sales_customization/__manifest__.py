{
    'name' : 'Advanced Sales Customization',
    'version' : '1.0',
    'author' : 'Aronno Chowdhury',
    'category' : 'Sales',
    'summary' : 'Advanced Sales Comunication and Custom Dashboard',
    'depends' : ['sale_management', 'web',],
    'data' : [
        'views/sales_order_views.xml',
    ],
    'assets' : {
        'web.assets_backend' : [
            'sales_customization/static/src/scss/custom_style.scss',
        ]
    },
    'application' : False,
    'installable' : True,
}
