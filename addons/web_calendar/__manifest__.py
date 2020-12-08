# -*- coding: utf-8 -*-
# Part of Byte. See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Calendar',
    'category': 'Hidden',
    'description':"""
Byte  ERP Web Calendar view.
==========================

""",
    'author': 'Byte  ERP SA, Valentino Lab (Kalysto)',
    'version': '2.0',
    'depends': ['web'],
    'data' : [
        'views/web_calendar_templates.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'auto_install': True
}
