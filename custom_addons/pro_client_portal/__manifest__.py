# -*- coding: utf-8 -*-
{
    'name': "Pro Client Portal",
    'summary': 'Custom client portal for proffessional communication',
    'description': """
        This module provides a custom client portal for professional communication, allowing clients to access their information, communicate with the comoany, and manage their interactions in a secure and user-friendly environment.
    """,
    'author': "Aronno Chowdhury",
    'website': "https://www.aronnoChowdhury.com",
    'category': 'Website',
    'version': '1.0',
    'depends': ['website', 'crm', 'project'],
    'installable': True,
    'application': True,
    'data': [
        'views/pro_header.xml',
        'views/portal_templates.xml',
    ],
}
