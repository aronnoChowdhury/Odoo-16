{
    'name': 'Telecom Plus',
    'version': '1.0.0',
    'summary': 'Custom website theme for Plus Telecom',
    'description': """
Plus Telecom Website Theme
===========================
This module provides a custom website layout and design for Plus Telecom.
    """,
    'author': 'Aronno Chowdhury',
    'website': 'https://www.telecomplus.com',
    'category': 'Website',
    'depends': ['website','base','web', 'crm'],
    'data': [
        'views/plus_header.xml',
        'views/plus_footer.xml',
        "views/hero.xml",
        "views/second.xml",
        "views/third.xml",
        "views/forth.xml",
        "views/fifth.xml",
        "views/sixth.xml",
        "views/seventh.xml",
        "views/eighth.xml",
        "views/ninth.xml",
        "views/tenth.xml",
        "views/service.xml",
        "views/shop.xml",
        "views/solution.xml",
        "views/about.xml",
        "views/contact.xml",
        "views/plus_snippets.xml",
        "views/login_template.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            "telecom_plus/static/src/scss/style.scss",
        ],
        'web.assets_backend': [
            "telecom_plus/static/src/scss/style.scss",
        ]
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
