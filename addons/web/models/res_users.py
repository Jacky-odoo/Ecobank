from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'
    is_app_user = fields.Boolean(default=False, readonly=True)
