# -*- coding: utf-8 -*-
# Part of Byte. See LICENSE file for full copyright and licensing details.

{
    'name': 'Tours',
    'category': 'Hidden',
    'description': """
Byte Erp Web tours.
========================

""",
    'version': '0.1',
    'depends': ['web'],
    'data': [
        'security/ir.model.access.csv',
        'views/tour_templates.xml',
        'views/tour_views.xml'
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'auto_install': True
}
