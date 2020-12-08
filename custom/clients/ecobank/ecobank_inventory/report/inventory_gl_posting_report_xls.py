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


IR_TRANSLATION_NAME = 'inventory.gl.posting.xlsx'


class InventoryGLPostingXlsx(AbstractReportXlsx):

    def _(self, src):
        lang = self.env.context.get('lang', 'en_US')
        val = translate(
            self.env.cr, IR_TRANSLATION_NAME, 'report', lang, src) or src
        return val

    def _get_ws_params(self, wb, data, wiz):
        self.branches = self.env['inventory.branch'].search([])
        self.wiz = wiz
        self.totals = 0.0
        self.stock_value = sum(wiz.env['inventory.item'].search([]).mapped('value'))
        s1 = self._get_inventory_gl_posting_ws_params(wb, data, wiz)
        return [s1]

    def _get_branch_template(self):

        branch_template = {
            'name': {
                'header': {
                    'type': 'string',
                    'value': self._('Branch'),
                },
                'branch': {
                    'type': 'string',
                    'value': self._render(
                        "branch.name"),
                },
                'grand_total': {
                    'type': 'string',
                    'value': self._(' Grand Totals'),
                },
                'stock_value': {
                    'type': 'string',
                    'value': self._('Current Stock Value'),
                },
                'width': 20,
            },
            'account_id': {
                'header': {
                    'type': 'string',
                    'value': self._('Account'),
                },
                'branch': {
                    'type': 'string',
                    'value': self._render(
                        "branch.account_id.name_and_code"),
                },

                'stock_value': {
                    'type': 'number',
                    'value': self._render("stock_value"),
                },
                'width': 40,
            },
            'debit': {
                'header': {
                    'type': 'string',
                    'value': self._('Debit'),
                },
                'branch': {
                    'type': 'number',
                    'value': self._render(
                        "total_amount"),
                },
                'grand_total': {
                    'type': 'number',
                    'value': self._render("grand_total"),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 20,
            },
            'credit': {
                'header': {
                    'type': 'string',
                    'value': self._('Credit (SLL116030001)'),
                },
                'branch': {
                    'type': 'number',
                    'value': self._render(
                        "total_amount"),
                },
                'grand_total': {
                    'type': 'number',
                    'value': self._render("grand_total"),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 20,
            }
        }
        branch_template.update( self.env['inventory.branch']._xls_inventory_gl_posting_template())

        return branch_template

    def _get_inventory_gl_posting_ws_params(self, wb, data, wiz):

        branch_template = self._get_branch_template()
        branch_template.update(
            self.env['inventory.branch']._xls_inventory_gl_posting_template())
        wl_act = self.env['inventory.branch']._xls_inventory_gl_posting_fields()
        date = wiz.date_to
        date_dt = datetime.strptime(date, '%Y-%m-%d')

        return {
            'ws_name': "GL Posting",
            'generate_ws_method': '_inventory_gl_posting_report',
            'title': "GL Posting as at "+str(date_dt.strftime("%B").upper()+" "+str(date_dt.day)+", "+str(date_dt.year)),
            'wanted_list': wl_act,
            'col_specs': branch_template,
        }

    def _report_title(self, ws, row_pos, ws_params, data, wiz):
        return self._write_ws_title(ws, row_pos, ws_params)

    def _inventory_gl_posting_report(self, workbook, ws, ws_params, data, wiz):
        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers['standard'])
        ws.set_footer(self.xls_footers['standard'])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        row_pos = self._report_title(ws, row_pos, ws_params, data, wiz)

        actives = self.env['inventory.branch'].search(
            [('id', 'in', self.branches.ids)],
            order='name ASC')

        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='header',
            default_format=self.format_theader_yellow_left)

        ws.freeze_panes(row_pos, 0)

        for branch in actives:
            self.totals += branch.get_gl_posting(wiz.date_to)
            row_pos = self._write_line(
                ws, row_pos, ws_params, col_specs_section='branch',
                render_space={
                    'branch': branch,
                    'total_amount': branch.get_gl_posting(wiz.date_to),
                    },
                default_format=self.format_tcell_left)

        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='grand_total',
            render_space={
                'grand_total': self.totals,

            },
            default_format=self.format_theader_yellow_left)

        row_pos = self._write_line(
            ws, row_pos, ws_params)

        row_pos = self._write_line(
            ws, row_pos, ws_params)

        self._write_line(
            ws, row_pos, ws_params, col_specs_section='stock_value',
            render_space={
                'stock_value': self.stock_value,

            })


InventoryGLPostingXlsx(
    'report.inventory.gl.posting.xlsx',
    'wiz.inventory.gl.posting',
    parser=report_sxw.rml_parse)
