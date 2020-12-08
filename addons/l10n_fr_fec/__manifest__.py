#-*- coding:utf-8 -*-
# Part of Byte. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2013-2015 Akretion (http://www.akretion.com)

{
    'name': 'France - FEC',
    'category': 'Localization',
    'summary': "Fichier d'Échange Informatisé (FEC) for France",
    'author': "Akretion,Byte  ERP Community Association (OCA)",
    'website': 'http://www.akretion.com',
    'depends': ['l10n_fr', 'account_accountant'],
    'data': [
        'wizard/account_fr_fec_view.xml',
    ],
    'auto_install': True,
}
