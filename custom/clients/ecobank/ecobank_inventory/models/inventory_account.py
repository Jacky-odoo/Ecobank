from odoo import api, fields, models
from odoo.exceptions import ValidationError


class InventoryUser(models.Model):
    _name = 'inventory.account'
    _rec_name = 'name_and_code'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    name_and_code = fields.Char(compute='compute_name_code', store=True)

    @api.multi
    @api.depends('name', 'code')
    def compute_name_code(self):
        for rec in self:
            if rec.code and rec.name:
                rec.name_and_code = str(rec.name + " (" + rec.code + ")")

    @api.multi
    def copy(self, default=None):
        raise ValidationError("Sorry you are not allowed to perform this operation. Error Code BYT001")

    @api.constrains('name')
    def check_name(self):
        all_accounts = self.search([])
        for account in all_accounts:
            if self.name.lower() == account.name.lower() and self.id != account.id:
                raise ValidationError("Error! Account Name already exist. BYT005")

    _sql_constraints = [
        ('unique_code', 'unique (code)', "Account Code Already Exist !"),
    ]
