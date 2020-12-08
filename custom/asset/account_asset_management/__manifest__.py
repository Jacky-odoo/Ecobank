# -*- coding: utf-8 -*-
# Copyright 2009-2018 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Assets Management',
    'version': '10.0.3.0.1',
    'license': 'AGPL-3',
    'depends': [
        'account_fiscal_year',
    ],
    'conflicts': ['account_asset'],
    'author': "Noviat,Byte  ERP Community Association (OCA)",
    'website': 'http://www.noviat.com',
    'category': 'Accounting & Finance',
    'sequence': 32,
    'data': [
        'security/account_asset_security.xml',
        'security/ir.model.access.csv',
        'wizard/account_asset_compute.xml',
        'wizard/account_asset_remove.xml',
        'views/account_account.xml',
        'views/account_asset.xml',
        'views/account_asset_profile.xml',
        'views/account_config_settings.xml',
        'views/account_invoice.xml',
        'views/account_invoice_line.xml',
        'views/account_move.xml',
        'views/account_move_line.xml',
        'views/account_asset_user.xml',
        'views/menuitem.xml',
        'report/asset_details_report_template.xml',
        'report/reports.xml',
        'data/sequence.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
