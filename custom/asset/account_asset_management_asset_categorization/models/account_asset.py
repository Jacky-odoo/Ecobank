# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountAsset(models.Model):
    _inherit = 'account.asset'
    asset_unit_id = fields.Many2one('asset.unit',
                                    'Unit', readonly=True,
                                    ondelete='restrict',
                                    states={'draft': [('readonly', False)]},)
    asset_department_id = fields.Many2one('asset.department', 'Department', readonly=True,
                                          ondelete='restrict',
                                          states={'draft': [('readonly', False)]},)
    sub_category_id = fields.Many2one('account.sub.category',
                                      string='Sub Category', readonly=True,
                                      required=True,
                                      ondelete='restrict',
                                      states={'draft': [('readonly', False)]},
                                      domain="['|', ('is_other', '=', True), ('category_id', '=', profile_id)]")
