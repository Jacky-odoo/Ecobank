from odoo import api, fields, models


class AccountAssetProfile(models.Model):
    _inherit = 'account.asset.profile'
    mutable_depreciation = fields.Boolean(string='Mutable Depreciation')
