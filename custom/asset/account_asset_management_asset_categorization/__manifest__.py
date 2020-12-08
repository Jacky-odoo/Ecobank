# -*- coding: utf-8 -*-
{
    'name': "Asset Management Asset Categorization",
    'author': "Francis Bangura <francis@byteltd.com>",
    'website': "http://www.byteltd.com",
    'category': 'Accounting & Finance',
    'version': '10.0.1.0.0',

    'depends': ['account_asset_management'],

    'data': [
        'security/ir.model.access.csv',
        'views/account_asset_asset_department.xml',
        'views/account_asset_asset_sub_category.xml',
        'views/account_asset_asset_unit.xml',
    ],
    
}
