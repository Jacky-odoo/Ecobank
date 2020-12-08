# -*- coding: utf-8 -*-
# © 2018-Today Aktiv Software (http://www.aktivsoftware.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import http
from odoo.http import request


class Home(http.Controller):
    """A new method is added."""

    @http.route('/web/get_datetime', type='json', auth="public")
    def get_datetime(self):
        """Format of date will be fetched on basis of company."""
        final_clock_format = None
        if request.context.get('uid'):
            final_clock_format = request.env['res.users'].browse(
                request.context.get('uid')).company_id.clock_format
        return final_clock_format
