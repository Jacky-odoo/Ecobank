{
    'name': "Asset UI",

    'summary': """Asset Management User Interface""",


    'author': "Byte Limited",
    'website': "http://byteltd.com",
    'category': 'Accounting & Finance',
    'version': '0.1',

    'depends': ['account_asset_management_xls',
                'account_accountant',
                'max_web_freeze_list_view_header',
                'account_asset_management_import',
                'account_asset_management_asset_categorization',
                'account_asset_management_location'],

    'data': [
        'asset_views.xml',
    ],
}
