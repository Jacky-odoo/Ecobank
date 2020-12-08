# -*- coding: utf-8 -*-
from odoo import fields, models


class AssetDepartment(models.Model):
    _name = 'asset.department'
    name = fields.Char('Department Name', required=True)
    code = fields.Char('Department Code', required=True)
    _sql_constraints = [('name_unique', 'unique(name)', 'Asset Department must be Unique!'),
                        ('code_unique', 'unique(code)', 'Asset Department Code must be Unique!')]
