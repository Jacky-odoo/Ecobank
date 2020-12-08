{
    'name': 'Asset Report',
    'version': '10.0.1.0.0',
    'category': 'Asset Report',
    'license': 'AGPL-3',
    'summary': 'Asset Report',
    'author': ' Francis Bangura<francis@byteltd.com>, ',
    'website': 'http://byteltd.com',
    'depends': ['report_xls'],
    'data': [
        'wizard/wiz_print_asset_report.xml',
        'data/data_asset_report.xml',
        'views/print_asset_report.xml',
    ],
    'installable': True,
}
