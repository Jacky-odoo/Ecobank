# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountAsset(models.Model):
    _inherit = "account.asset"
    
    location_id = fields.Many2one('account.asset.location', readonly=True,
                                  ondelete='restrict',
                                  states={'draft': [('readonly', False)]},
                                  string="Asset Location", track_visibility="onchange")
    location_move_ids = fields.One2many('account.asset.location.move', 'asset_id')

    relocation_count = fields.Integer(string="Number of relocations",
                                      compute='_relocation_count', readonly=True, store=True)

    @api.one
    @api.depends('location_move_ids')
    def _relocation_count(self):
        self.relocation_count = len(self.location_move_ids.filtered(lambda r: r.state == 'done'))
