from odoo import models, fields, api
from datetime import date


class AccountAsset(models.Model):
    _inherit = 'account.asset'
    depreciation_expense_account_id = fields.Many2one('account.account',
                                                      required=True,
                                                      ondelete='restrict',
                                                      string='Depreciation Expense Account',
                                                      help='Select Depreciation Expense Account for this asset',
                                                      domain="[('is_depreciation_expense_account','=',True)]")
    accumulated_depreciation_account_id = fields.Many2one('account.account',
                                                          required=True,
                                                          ondelete='restrict',
                                                          string='Accumulated Depreciation Account',
                                                          help='Select Accumulated Depreciation Account for this asset',
                                                          domain="[('is_accumulated_depreciation_account','=',True)]")
    asset_gl_account_id = fields.Many2one('account.account',
                                          required=True,
                                          string='Asset GL',
                                          ondelete='restrict',
                                          help='Select Accumulated Depreciation Account for this asset',
                                          domain="[('is_asset_gl','=',True)]")

    vendor = fields.Char(string="Vendor")
    serial_no = fields.Char(string="Serial No")

    legacy_sys_no = fields.Char(string='Legacy Sys No.')

    @api.multi
    def compute_asset_depr(self):
        all_assets = self.env['account.asset'].search([])
        done = []
        for asset in all_assets:
            if asset.depreciation_line_ids:
                asset_depre = asset.depreciation_line_ids.filtered(lambda x: fields.Date.from_string(x.line_date) < date.today())
                if len(asset_depre) > 1:
                    for depr in asset_depre:
                        depr.create_move()
            done.append(asset)
        return True
