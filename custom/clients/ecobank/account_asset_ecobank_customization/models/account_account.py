from odoo import fields, models, api
from odoo.exceptions import UserError


class AccountAccount(models.Model):
    _inherit = 'account.account'
    _rec_name = 'code'

    is_depreciation_expense_account = fields.Boolean(default=False,
                                                     string='Is Depreciation Expense Account')

    is_accumulated_depreciation_account = fields.Boolean(default=False,
                                                         string='Is Accumulated Depreciation Account')
    is_asset_gl = fields.Boolean(default=False, string='Is Asset GL')
    description = fields.Char(string='Description',
                              compute='compute_description',
                              store=True)

    @api.multi
    @api.depends('code')
    def name_get(self):
        result = []
        for account in self:
            name = account.code
            result.append((account.id, name))
        return result

    @api.multi
    def unlink(self):
        for account in self:
            assets_depr = self.env['account.asset'].search([('depreciation_expense_account_id', '=', account.id)])
            assets_accum = self.env['account.asset'].search([('accumulated_depreciation_account_id', '=', account.id)])
            assets_gl = self.env['account.asset'].search([('asset_gl_account_id', '=', account.id)])
            if assets_depr:
                msg = 'You cannot delete an account that ' \
                      'is used as a Depreciation Expense Account by assets in the system.' \
                      ' These are the asset(s) : \n'
                for asset in assets_depr:
                    msg += 'Description: "%s" Sys. No: %s \n' % (
                        asset.name, asset.sys_no
                    )
                raise UserError(msg)
            if assets_accum:
                msg = 'You cannot delete an account that ' \
                      'is used as an Accumulated Depreciation Account by assets in the system.' \
                      ' These are the asset(s) : \n'
                for asset in assets_accum:
                    msg += 'Description: "%s" Sys. No: %s \n' % (
                        asset.name, asset.sys_no
                    )
                raise UserError(msg)
            if assets_gl:
                msg = 'You cannot delete an account that ' \
                      'is used a GL Account by assets in the system.' \
                      ' These are the asset(s) : \n'
                for asset in assets_gl:
                    msg += 'Description: "%s" Sys. No: %s \n' % (
                        asset.name, asset.sys_no
                    )
                raise UserError(msg)
        super(AccountAccount, self).unlink()

    @api.multi
    @api.depends('is_depreciation_expense_account', 'is_accumulated_depreciation_account')
    def compute_description(self):
        for rec in self:
            if rec.is_accumulated_depreciation_account:
                rec.description = 'Accumulated Depreciation'
            if rec.is_depreciation_expense_account:
                rec.description = 'Depreciation Expense'

    @api.multi
    def get_month_accumulated_depreciation(self, date):
        total = 0.0
        for rec in self:
            assets = self.env['account.asset'].search([('depreciation_expense_account_id', '=', rec.id),
                                                       ('type', '=', 'normal'),
                                                       ('state', '!=', 'draft'),
                                                       ('date_start', '<=', date)])
            if len(assets) > 0:
                for asset in assets:
                    if asset.type == 'normal':
                        total += asset.get_month_depreciation(date)
        return total

    @api.multi
    def get_month_depreciation(self, date):
        total = 0.0
        for rec in self:
            assets = self.env['account.asset'].search([('accumulated_depreciation_account_id', '=', rec.id),
                                                       ('type', '=', 'normal'),
                                                       ('state', '!=', 'draft'),
                                                       ('date_start', '<=', date)])
            if len(assets) > 0:
                for asset in assets:
                    if asset.type == 'normal':
                        total += asset.get_month_depreciation(date)
        return total

    @api.model
    def _xls_account_template(self):
        """
        Template updates

        """
        return {}

    @api.model
    def _xls_gl_posting_template(self):
        """
        Template updates

        """
        return {}

    @api.model
    def _xls_gl_posting_fields(self):
        """
        Update list in custom module to add/drop columns or change order
        """
        return [
            'code', 'description', 'credit', 'debit'
        ]
