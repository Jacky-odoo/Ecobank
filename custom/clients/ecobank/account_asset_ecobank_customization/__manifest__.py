{
    'name': "Asset Ecobank Customization",

    'summary': """Asset Management Ecobank Customization""",


    'author': "Byte Limited",
    'website': "http://byteltd.com",
    'category': 'Accounting & Finance',
    'version': '0.1',

    'depends': ['account_asset_ui'],

    'data': [
        'views/account_asset.xml',
        'views/account_account.xml',
        'views/account_asset_profile.xml',
        #'report/asset_details_report.xml',
        #'report/asset_details_report_template.xml',
        'wizard/wiz_gl_posting_report.xml',
    ],
}
