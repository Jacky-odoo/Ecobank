# -*- coding: utf-8 -*-
# Copyright 2009-2018 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.report_xlsx_helper.report.abstract_report_xlsx \
    import AbstractReportXlsx
from odoo.report import report_sxw
from odoo.tools.translate import translate, _
from datetime import datetime

_logger = logging.getLogger(__name__)


IR_TRANSLATION_NAME = 'account.gl.posting.xlsx'
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


class AssetGlPostingXlsx(AbstractReportXlsx):

    def _(self, src):
        lang = self.env.context.get('lang', 'en_US')
        val = translate(
            self.env.cr, IR_TRANSLATION_NAME, 'report', lang, src) or src
        return val

    def _get_ws_params(self, wb, data, wiz):
        self.accounts = self.env['account.account'].search(['|', ('is_depreciation_expense_account', '=', True),
                                                            ('is_accumulated_depreciation_account', '=', True)])
        self.total_depreciation = 0
        self.total_accumulation = 0
        self.wiz = wiz
        s1 = self._get_gl_posting_ws_params(wb, data, wiz)
        return [s1]

    def _get_account_template(self):

        account_template = {
            'code': {
                'header': {
                    'type': 'string',
                    'value': self._('Account Number'),
                },
                'account': {
                    'type': 'string',
                    'value': self._render(
                        "account.code"),
                },
                'totals': {
                    'type': 'string',
                    'value': self._(' Grand Totals'),
                },
                'width': 20,
            },
            'description': {
                'header': {
                    'type': 'string',
                    'value': self._('Account Name'),
                },
                'account': {
                    'value': self._render(
                        "description"),
                    'format': self.format_tcell_date_left,
                },
                'width': 40,
            },
            'debit': {
                'header': {
                    'type': 'string',
                    'value': self._('Debit'),
                },
                'account': {
                    'type': 'number',
                    'value': self._render("accumulated"),
                },
                'totals': {
                    'type': 'number',
                    'value': self._render("acc"),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 18,
            },
            'credit': {
                'header': {
                    'type': 'string',
                    'value': self._('Credit'),
                },
                'account': {
                    'type': 'number',
                    'value': self._render("depreciation"),
                },
                'totals': {
                    'type': 'number',
                    'value': self._render("grand_total"),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 18,
            }

        }
        account_template.update(
            self.env['account.account']._xls_account_template())

        return account_template

    def _get_gl_posting_ws_params(self, wb, data, wiz):

        depreciation_template = self._get_account_template()
        depreciation_template.update(
            self.env['account.account']._xls_gl_posting_template())
        wl_act = self.env['account.account']._xls_gl_posting_fields()
        date = wiz.date_to
        date_dt = datetime.strptime(date, '%Y-%m-%d')

        return {
            'ws_name': "GL Posting Report",
            'generate_ws_method': '_depreciation_expense_report',
            'title': "GL Posting for "+str(date_dt.strftime("%B").upper()+", "+str(date_dt.year)),
            'wanted_list': wl_act,
            'col_specs': depreciation_template,
        }

    def _report_title(self, ws, row_pos, ws_params, data, wiz):
        return self._write_ws_title(ws, row_pos, ws_params)

    def _empty_report(self, ws, row_pos, ws_params, data, wiz, report):
        if report == 'acquisition':
            suffix = _('New Acquisitions')
        elif report == 'active':
            suffix = _('Active Assets')
        else:
            suffix = _('Removed Assets')
        no_entries = _("No") + " " + suffix
        ws.write_string(row_pos, 0, no_entries, self.format_left_bold)

    def _view_add(self, acq, accounts):
        accounts.append(acq)

    def _depreciation_expense_report(self, workbook, ws, ws_params, data, wiz):
        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers['standard'])
        ws.set_footer(self.xls_footers['standard'])

        wl_act = ws_params['wanted_list']

        self._set_column_width(ws, ws_params)

        row_pos = 0
        row_pos = self._report_title(ws, row_pos, ws_params, data, wiz)

        actives = self.env['account.account'].search(
            [('id', 'in', self.accounts.ids)],
            order='description DESC')

        if not actives:
            return self._empty_report(
                ws, row_pos, ws_params, data, wiz, 'active')

        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='header',
            default_format=self.format_theader_yellow_left)

        ws.freeze_panes(row_pos, 0)

        acts = self.accounts.filtered(lambda r: r in actives)
        acts_and_parents = []
        for act in acts:
            self._view_add(act, acts_and_parents)

        entries = []
        for account in acts:
            entry = {}

            entry['account'] = account
            entries.append(entry)
        for entry in entries:
            account = entry['account']
            depreciation = account.get_month_depreciation(wiz.date_to)
            accumulated = account.get_month_accumulated_depreciation(wiz.date_to)

            self.total_depreciation += depreciation
            self.total_accumulation += accumulated

            row_pos = self._write_line(
                ws, row_pos, ws_params, col_specs_section='account',
                render_space={
                    'account': account,
                    'description': account.description,
                    'depreciation': depreciation,
                    'accumulated': accumulated,
                    'acc': accumulated,
                    'depr': depreciation,

                    },
                default_format=self.format_tcell_left)

        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='totals',
            render_space={
                'acc': self.total_accumulation,
                'depr': self.total_depreciation,
                'grand_total':self.total_depreciation,

            },
            default_format=self.format_theader_yellow_left)


AssetGlPostingXlsx(
    'report.account.gl.posting.xlsx',
    'wiz.gl.posting.report',
    parser=report_sxw.rml_parse)
