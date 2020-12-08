# -*- coding: utf-8 -*-
from odoo import models, api, exceptions, SUPERUSER_ID

MODULE_NAME = 'ir_rule_protected'


class Module(models.Model):
    _inherit = "ir.module.module"

    @api.multi
    def button_uninstall(self):
        for r in self:
            if r.name == MODULE_NAME and self.env.uid != SUPERUSER_ID:
                raise exceptions.Warning("Only admin can uninstall the module")
        return super(Module, self).button_uninstall()
