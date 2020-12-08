# -*- coding: utf-8 -*-
# Copyright 2009-2018 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date
import calendar

_CALENDER_MONTHS = [
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
]


class WizAssetRegisterReport(models.TransientModel):

    _name = 'wiz.asset.register.report'
    _description = 'Assets Depreciation Expense report'

    def _current_month(self):
        return date.today().month

    @api.onchange('month')
    @api.multi
    def onchange_month(self):
        for rec in self:
            if rec.month:
                year = date.today().year
                weekday, end_date = calendar.monthrange(year, rec.month)
                rec.date_to = fields.Date.from_string((str(year)+"-"+str(rec.month) +"-"+str(end_date)))

    month = fields.Selection(
        [(1, 'January'), (2, 'February'),
            (3, 'March'),
            (4, 'April'),
            (5, 'May'),
            (6, 'June'),
            (7, 'July'),
            (8, 'August'),
            (9, 'September'),
            (10, 'October'),
            (11, 'November'),
            (12, 'December'), ],
        default=date.today().month
    )
    date_to = fields.Date(
        'To Date',
        required=True,
    )

    @api.multi
    def xls_export(self):
        self.ensure_one()
        asset_obj = self.env['account.asset']
        domain = [('type', '=', 'normal')]
        assets = asset_obj.search(domain)
        if not assets:
            raise UserError(
                _('No records found for your selection!'))

        report = {
            'type': 'ir.actions.report.xml',
            'report_type': 'xlsx',
            'report_name': 'account.asset.register.xlsx',
            'context': dict(self._context, xlsx_export=True),
            'datas': {'ids': [self.id]},
        }
        return report
