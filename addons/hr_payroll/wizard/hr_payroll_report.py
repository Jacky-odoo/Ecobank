# -*- coding: utf-8 -*-
# Copyright 2009-2018 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class WizPayrollReport(models.TransientModel):

    _name = 'wiz.payroll.report'
    _description = 'Payroll Excel Report'

    payslip_run_id = fields.Many2one('hr.payslip.run', string='Select Payroll')

    @api.multi
    def xls_export(self):
        self.ensure_one()
        if not self.payslip_run_id.slip_ids:
            raise UserError(
                _('No Payslips found for in this payroll!'))

        report = {
            'type': 'ir.actions.report.xml',
            'report_type': 'xlsx',
            'report_name': 'payroll.report.xlsx',
            'context': dict(self._context, xlsx_export=True),
            'datas': {'ids': [self.id]},
        }
        return report
