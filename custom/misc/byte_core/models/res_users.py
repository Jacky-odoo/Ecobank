from odoo import models, api, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def write(self, values):
        return super(ResUsers, self).write(values)
