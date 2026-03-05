{
    'name': 'Pulse Theme',
    'version': '16.0.1.0.0',
    'summary': 'Custom website theme for Pulse Telecom',
    'description': """
Pulse Telecom Website Theme
===========================
This module provides a custom website layout and design for Pulse Telecom.
    """,
    'author': 'Aronno Chowdhury',
    'website': 'https://www.pulsetelecom.com',
    'category': 'Website',
    'depends': ['website','base'],
    'data': [
        'views/header.xml',
        'views/footer.xml',
        'views/hero_template.xml',
        'views/features_template.xml',
        'views/shop_details.xml',
        'views/shop_template.xml',
        'views/contact.xml',
        'views/snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'pulse_theme/static/src/scss/style.scss',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
