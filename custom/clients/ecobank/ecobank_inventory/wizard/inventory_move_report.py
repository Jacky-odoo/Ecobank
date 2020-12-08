from odoo import models, api, fields
from odoo.exceptions import ValidationError
from datetime import date
import calendar


_CALENDER_MONTHS = (
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
)


class InventoryMove(models.TransientModel):
    _name = 'wiz.inventory.move'

    def current_month(self):
        return date.today().month

    month = fields.Selection(
        _CALENDER_MONTHS,
        default=current_month
    )
    date_from = fields.Date(
        'From Date',
        required=True,
    )
    date_to = fields.Date(
        'To Date',
        required=True,
    )
    move_type = fields.Selection([('issue', 'Issue'), ('receipt', 'Receipt'), ('both', 'Issue and Receipt')],
                                 default='issue',
                                 string='Move Type',
                                 required=True)

    @api.constrains('date_from', 'date_to')
    @api.one
    def _check_date(self):
        if self.date_from > self.date_to:
            raise ValidationError('Date from can not be greater than date to')

    @api.onchange('month')
    @api.multi
    def onchange_month(self):
        for rec in self:
            if rec.month:
                year = date.today().year
                weekday, end_date = calendar.monthrange(year, rec.month)
                date_from = date(year, rec.month, 1)
                date_to = date(year, rec.month, end_date)
                rec.update({'date_from': fields.Date.to_string(date_from),
                            'date_to': fields.Date.to_string(date_to)})

    def print_report(self):
        domain = [('date', '>=', self.date_from), ('date', '<=', self.date_to)]
        if self.move_type == 'receipt':
            receipt_lines = self.env['inventory.addition.line'].search(domain)
            if len(receipt_lines) < 1:
                raise ValidationError("No Move Lines to report on")
        if self.move_type == 'issue':
            issue_lines = self.env['inventory.subtraction.line'].search(domain)
            if len(issue_lines) < 1:
                raise ValidationError("No Move Lines to report on")
        if self.move_type == 'both':
            receipt_lines = self.env['inventory.addition.line'].search(domain)
            issue_lines = self.env['inventory.subtraction.line'].search(domain)
            if len(issue_lines) < 1 and len(receipt_lines) < 1:
                raise ValidationError("No Move Lines to report on")

        report = {
            'type': 'ir.actions.report.xml',
            'report_type': 'xlsx',
            'report_name': 'inventory.moves.xlsx',
            'context': dict(self._context, xlsx_export=True),
            'datas': {'ids': [self.id]},
        }
        return report
