# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions, SUPERUSER_ID

MODULE_NAME = 'ir_rule_protected'


class IRRule(models.Model):
    _inherit = 'ir.rule'

    protected = fields.Boolean('Protected', help='Make rule editable only for superuser')

    @api.multi
    def check_restricted(self):
        if self.env.user.id == SUPERUSER_ID:
            return
        for r in self:
            if r.protected:
                raise exceptions.Warning("The Rule is protected. You don't have access for this operation")

    @api.multi
    def write(self, vals):
        self.check_restricted()
        return super(IRRule, self).write(vals)

    @api.multi
    def unlink(self):
        self.check_restricted()
        return super(IRRule, self).unlink()


class Module(models.Model):
    _inherit = "ir.module.module"

    def button_uninstall(self):
        user = self.env.user.id
        for module in self:
            if module.name == MODULE_NAME and user != SUPERUSER_ID:
                raise exceptions.Warning("Only admin can uninstall the module")
        return super(Module, self).button_uninstall()




