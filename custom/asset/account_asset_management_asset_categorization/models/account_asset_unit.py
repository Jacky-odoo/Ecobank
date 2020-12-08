# -*- coding: utf-8 -*-
from odoo import fields, models


class AssetUnit(models.Model):
    _name = 'asset.unit'
    name = fields.Char('Asset Unit', required=True)
    code = fields.Char('Unit Code', required=True)
    _sql_constraints = [('name_unique', 'unique(name)', 'Asset Unit must be Unique!'),
                        ('code_unique', 'unique(code)', 'Asset Unit Code must be Unique!')]
