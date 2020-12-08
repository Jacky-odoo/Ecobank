from odoo import models, api, fields
from odoo.exceptions import ValidationError
from datetime import date


class InventoryBalance(models.TransientModel):
    _name = 'wiz.inventory.balance'
    date = fields.Date(string='Date', default=date.today())

    def print_inventory_balance(self):
        items = self.env['inventory.item'].search([])
        if len(items) < 1:
            raise ValidationError("There are no items to report on")
        if fields.Date.from_string(self.date) > date.today():
            raise ValidationError("You cannot select a date in the future")

        report = {
            'type': 'ir.actions.report.xml',
            'report_type': 'xlsx',
            'report_name': 'inventory.balance.xlsx',
            'context': dict(self._context, xlsx_export=True),
            'datas': {'ids': [self.id]},
        }
        return report
