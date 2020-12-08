# -*- coding: utf-8 -*-
# Part of Byte. See LICENSE file for full copyright and licensing details.

{
    'name': 'Web',
    'category': 'Hidden',
    'version': '1.0',
    'description':
        """
Byte Erp Web core module.
========================

This module provides the core of the Byte Erp Web Client.
        """,
    'depends': ['base'],
    'auto_install': True,
    'data': [
        'views/webclient_templates.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'bootstrap': True,  # load translations for login screen
}
