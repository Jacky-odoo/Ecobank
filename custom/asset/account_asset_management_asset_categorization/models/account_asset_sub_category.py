# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class AssetSubCategory(models.Model):
    _name = 'account.sub.category'
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    is_other = fields.Boolean(string='is Other')
    category_id = fields.Many2one('account.asset.profile', string='Category')
    _sql_constraints = [('name_unique', 'unique(name)', 'Name must be Unique!'),
                        ('code_unique', 'unique(code)', 'Code must be Unique!')]

    @api.constrains('is_other', 'name')
    def check_other(self):
        for rec in self:
            if rec.is_other and not rec.name == "OTHER":
                raise ValidationError('Opertion not permitted, you cannot set this category  type as other. '
                                      'Name must be OTHER ')
