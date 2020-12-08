# -*- coding: utf-8 -*-
{
    'name': "Asset Location",

    'summary': """Adds Location And relocation to assets""",

    'author': "Francis Bangura(Byte Limited)",
    'website': "http://www.byteltd.com",
    'category': 'Accounting & Finance',
    'version': '10.0.1.0.0',

    'depends': ['account_asset_management'],

    'data': [
        'security/ir.model.access.csv',
        'views/account_asset_location.xml',
    ],
    
}
