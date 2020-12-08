from odoo import models, api, fields
from odoo.exceptions import ValidationError
import datetime


class InventoryBranch(models.Model):
    _name = 'inventory.branch'
    name = fields.Char(string='Name', required=True)
    account_id = fields.Many2one(comodel_name='inventory.account', string='Account',
                                 required=True,
                                 ondelete='restrict')

    @api.multi
    def copy(self, default=None):
        raise ValidationError("Sorry you are not allowed to perform this operation")

    @api.constrains('name')
    def check_name(self):
        all_branches = self.search([])
        for branch in all_branches:
            if self.name.lower() == branch.name.lower() and self.id != branch.id:
                raise ValidationError("Error! Branch already exist. BYT005")

    @api.model
    def _xls_inventory_gl_posting_fields(self):
        return ['name', 'account_id', 'debit', 'credit']

    @api.model
    def _xls_inventory_gl_posting_template(self):
        return {}

    @api.multi
    def get_gl_posting(self, date_to):
        month = fields.Date.from_string(date_to).month
        year = fields.Date.from_string(date_to).year
        date_from = fields.Date.to_string(datetime.date(year, month, 1))
        for rec in self:
            all_issues = self.env['inventory.subtraction.line'].search([('branch_id', '=', rec.id),
                                                                        ('date', '>=', date_from),
                                                                        ('date', '<=', date_to)])
            if len(all_issues):
                return float("%0.2f" % sum(all_issues.mapped('value')))
            else:
                return 0.0
