# -*- coding: utf-8 -*-
# Copyright 2009-2018 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.report_xlsx_helper.report.abstract_report_xlsx \
    import AbstractReportXlsx
from odoo.report import report_sxw
from odoo.tools.translate import translate, _
from datetime import date as date_obj
from datetime import datetime



IR_TRANSLATION_NAME = 'payroll.report.xlsx'


class PayrollReportXlsx(AbstractReportXlsx):

    def _(self, src):
        lang = self.env.context.get('lang', 'en_US')
        val = translate(
            self.env.cr, IR_TRANSLATION_NAME, 'report', lang, src) or src
        return val

    def _get_ws_params(self, wb, data, wiz):
        self.payslips = wiz.payslip_run_id.slip_ids

        self.wiz = wiz
        s1 = self._get_payroll_register_ws_params(wb, data, wiz)
        self.total_basic = 0
        self.total_gross = 0
        self.total_nassit = 0
        self.total_nassitte = 0
        self.total_paye = 0
        self.total_ded = 0
        self.total_net = 0
        return [s1]

    def _get_payslip_template(self):

        payslip_template = {
            'employee_name': {
                'header': {
                    'type': 'string',
                    'value': self._('Employee'),
                },
                'payslip': {
                    'type': 'string',
                    'value': self._render(
                        "payslip.employee_id.name"),
                },
                'totals': {
                    'type': 'string',
                    'value': self._('Totals'),
                },
                'width': 20,
            },
            'employee_id': {
                'header': {
                    'type': 'string',
                    'value': self._('Employee ID'),
                },
                'payslip': {
                    'type': 'string',
                    'value': self._render(
                        "payslip.employee_id.identification_id"),
                },
                'totals': {
                    'type': 'string',
                    'value': self._('Totals'),
                },
                'width': 20,
            },
            'employee_bank': {
                'header': {
                    'type': 'string',
                    'value': self._('Employee Bank'),
                },
                'payslip': {
                    'type': 'string',
                    'value': self._render(
                        "payslip.employee_id.bank_account_id and payslip.employee_id.bank_account_id.bank_id.name or ''"),
                },
                'totals': {
                    'type': 'string',
                    'value': self._('Totals'),
                },
                'width': 20,
            },
            'employee_bank_account': {
                'header': {
                    'type': 'string',
                    'value': self._('Employee Bank Account #'),
                },
                'payslip': {
                    'type': 'string',
                    'value': self._render(
                        "payslip.employee_id.bank_account_id and payslip.employee_id.bank_account_id.acc_number or ''"),
                },
                'totals': {
                    'type': 'string',
                    'value': self._('Totals'),
                },
                'width': 20,
            },
            'basic_sal': {
                'header': {
                    'type': 'string',
                    'value': self._('BASIC'),
                    'format': self.format_theader_yellow_right,
                },
                'payslip': {
                    'type': 'number',
                    'value': self._render('basic_sal'),
                    'format': self.format_tcell_amount_right,
                },
                'totals': {
                    'type': 'number',
                    'value': self._render("total_basic"),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 18,
            },
            'gross_sal': {
                'header': {
                    'type': 'string',
                    'value': self._('GROSS'),
                    'format': self.format_theader_yellow_right,
                },
                'payslip': {
                    'type': 'number',
                    'value': self._render('gross_sal'),
                    'format': self.format_tcell_amount_right,
                },
                'totals': {
                    'type': 'number',
                    'value': self._render("total_gross"),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 18,
            },
            'nassit_sal': {
                'header': {
                    'type': 'string',
                    'value': self._('NASSIT (5%)'),
                    'format': self.format_theader_yellow_right,
                },
                'payslip': {
                    'type': 'number',
                    'value': self._render('nassit_sal'),
                    'format': self.format_tcell_amount_right,
                },
                'totals': {
                    'type': 'number',
                    'value': self._render("total_nassit"),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 18,
            },
            'nassitte_sal': {
                'header': {
                    'type': 'string',
                    'value': self._('NASSIT (10%)'),
                    'format': self.format_theader_yellow_right,
                },
                'payslip': {
                    'type': 'number',
                    'value': self._render('nassitte_sal'),
                    'format': self.format_tcell_amount_right,
                },
                'totals': {
                    'type': 'number',
                    'value': self._render("total_nassitte"),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 18,
            },

            'paye_sal': {
                'header': {
                    'type': 'string',
                    'value': self._('PAYE'),
                    'format': self.format_theader_yellow_right,
                },
                'payslip': {
                    'type': 'number',
                    'value': self._render('paye_sal'),
                    'format': self.format_tcell_amount_right,
                },
                'totals': {
                    'type': 'number',
                    'value': self._render("total_paye"),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 18,
            },

            'total_ded': {
                'header': {
                    'type': 'string',
                    'value': self._('TOTAL DED'),
                    'format': self.format_theader_yellow_right,
                },
                'payslip': {
                    'type': 'number',
                    'value': self._render('total_ded'),
                    'format': self.format_tcell_amount_right,
                },
                'totals': {
                    'type': 'number',
                    'value': self._render("total_ded"),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 18,
            },


            'net_sal': {
                'header': {
                    'type': 'string',
                    'value': self._('NET'),
                    'format': self.format_theader_yellow_right,
                },
                'payslip': {
                    'type': 'number',
                    'value': self._render('net_sal'),
                    'format': self.format_tcell_amount_right,
                },
                'totals': {
                    'type': 'number',
                    'value': self._render("total_net"),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 18,
            },

        }
        payslip_template.update(
            self.env['hr.payslip']._xls_payslip_report_template())

        return payslip_template

    def _get_payroll_register_ws_params(self, wb, data, wiz):

        payroll_template = self._get_payslip_template()
        payroll_template.update(
            self.env['hr.payslip']._xls_payslip_report_template())
        wl_act = self.env['hr.payslip']._xls_payroll_report_fields()

        return {
            'ws_name': "Payroll Report",
            'generate_ws_method': '_payroll_report',
            'title': str(wiz.payslip_run_id.name)+" Payroll Register",
            'wanted_list': wl_act,
            'col_specs': payroll_template,
        }

    def _report_title(self, ws, row_pos, ws_params, data, wiz):
        return self._write_ws_title(ws, row_pos, ws_params)

    def _empty_report(self, ws, row_pos, ws_params, data, wiz, report):
        if report == 'acquisition':
            suffix = _('New Acquisitions')
        elif report == 'active':
            suffix = _('Employees')
        else:
            suffix = _('Removed Assets')
        no_entries = _("No") + " " + suffix
        ws.write_string(row_pos, 0, no_entries, self.format_left_bold)

    def _payroll_report(self, workbook, ws, ws_params, data, wiz):
        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers['standard'])
        ws.set_footer(self.xls_footers['standard'])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        row_pos = self._report_title(ws, row_pos, ws_params, data, wiz)

        actives = self.env['hr.payslip'].search(
            [('id', 'in', self.payslips.ids)])

        if not actives:
            return self._empty_report(
                ws, row_pos, ws_params, data, wiz, 'active')

        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='header',
            default_format=self.format_theader_yellow_left)

        ws.freeze_panes(row_pos, 0)

        for payslip in actives:
            self.total_basic += payslip.get_basic() or 0
            self.total_nassit += payslip.get_basic()*0.05 or 0
            self.total_nassitte += payslip.get_basic()*0.10 or 0
            self.total_gross += payslip.get_gross()
            self.total_paye += payslip.get_paye()
            self.total_ded += payslip.get_total_ded()
            self.total_net += payslip.get_net()

            row_pos = self._write_line(
                ws, row_pos, ws_params, col_specs_section='payslip',
                render_space={
                    'payslip': payslip,
                    'nassit_sal': payslip.get_basic()*0.05 or 0,
                    'nassitte_sal': payslip.get_basic()*0.10 or 0,
                    'gross_sal': payslip.get_gross() or 0,
                    'paye_sal': payslip.get_paye() or 0,
                    'basic_sal': payslip.get_basic() or 0,
                    'total_ded': payslip.get_total_ded() or 0,
                    'net_sal': payslip.get_net() or 0,
                    },
                default_format=self.format_tcell_left)
        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='totals',
            render_space={
                'total_basic': self.total_basic,
                'total_gross': self.total_gross,
                'total_nassit': self.total_nassit,
                'total_nassitte': self.total_nassitte,
                'total_paye': self.total_paye,
                'total_ded': self.total_ded,
                'total_net': self.total_net
            },
            default_format=self.format_theader_yellow_left)


PayrollReportXlsx(
    'report.payroll.report.xlsx',
    'wiz.payroll.report',
    parser=report_sxw.rml_parse)
