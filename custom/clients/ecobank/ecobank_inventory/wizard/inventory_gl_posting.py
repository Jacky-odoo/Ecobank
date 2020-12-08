from odoo import models, api, fields
from odoo.exceptions import ValidationError
from datetime import date
import calendar


class InventoryGlPosting(models.TransientModel):
    _name = 'wiz.inventory.gl.posting'
    date_to = fields.Date(string='Date', default=date.today())

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

    def print_inventory_gl_posting(self):
        items = self.env['inventory.branch'].search([])
        if len(items) < 1:
            raise ValidationError("There are no Branches to report on")

        report = {
            'type': 'ir.actions.report.xml',
            'report_type': 'xlsx',
            'report_name': 'inventory.gl.posting.xlsx',
            'context': dict(self._context, xlsx_export=True),
            'datas': {'ids': [self.id]},
        }
        return report
