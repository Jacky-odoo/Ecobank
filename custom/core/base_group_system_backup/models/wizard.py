# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BaseGroupSystemBackup(models.TransientModel):
    _name = 'base.group_system.backup'
    
    @api.multi
    def apply(self):
        self.ensure_one()
        return {
             'type' : 'ir.actions.act_url',
             'url': '/web/group_system_backup',
             'target': 'self',
        }
