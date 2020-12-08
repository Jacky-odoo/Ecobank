# -*- coding: utf-8 -*-
# Part of Byte. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class Website(models.Model):
    _inherit = "website"

    @api.model
    def payment_acquirers(self):
        return list(self.env['payment.acquirer'].sudo().search([('website_published', '=', True)]))
