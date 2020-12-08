from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'
    access_token = fields.Char(readonly=True)
    refresh_token = fields.Char(readonly=True)
