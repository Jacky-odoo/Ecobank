from odoo import api, models, fields
from odoo.addons.report_xlsx_helpers.report.abstract_report_xlsx import AbstractReportXlsx
_render = AbstractReportXlsx._render


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.multi
    def get_basic(self):
        return self.line_ids.filtered(lambda r: r.code == "BASIC").total

    @api.multi
    def get_gross(self):
        return self.line_ids.filtered(lambda r: r.code == "GROSS").total

    @api.multi
    def get_paye(self):
        paye = 0
        if self.line_ids.filtered(lambda r: r.code == "PAYE").total > 0:
            paye = self.line_ids.filtered(lambda r: r.code == "PAYE").total
        if self.line_ids.filtered(lambda r: r.code == "PAYE").total < 0:
            paye = self.line_ids.filtered(lambda r: r.code == "PAYE").total*-1
        if self.line_ids.filtered(lambda r: r.code == "WITHOLDING").total > 0:
            paye = self.line_ids.filtered(lambda r: r.code == "WITHOLDING").total
        if self.line_ids.filtered(lambda r: r.code == "WITHOLDING").total < 0:
            paye = self.line_ids.filtered(lambda r: r.code == "WITHOLDING").total*-1
        return paye

    @api.multi
    def get_total_ded(self):
        return self.line_ids.filtered(lambda r: r.code == "TOTALDED").total

    @api.multi
    def get_net(self):
        return self.line_ids.filtered(lambda r: r.code == "NET").total

    @api.model
    def _xls_payroll_report_fields(self):
        """
        Update list in custom module to add/drop columns or change order
        """
        return [
            'employee_name', 'employee_id',  'employee_bank',
            'employee_bank_account', 'basic_sal', 'gross_sal',
            'nassit_sal', 'nassitte_sal',
            'paye_sal', 'total_ded', 'net_sal'
        ]

    @api.model
    def _xls_payslip_report_template(self):
        """
        Template updates

        """
        return {}

