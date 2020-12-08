# -*- coding: utf-8 -*-
# © 2018-Today Aktiv Software (http://www.aktivsoftware.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    """A new field is added."""

    _inherit = 'res.company'

    clock_format = fields.Char(
        string="Clock Format", default="%M %b | %H:%M:%S")
