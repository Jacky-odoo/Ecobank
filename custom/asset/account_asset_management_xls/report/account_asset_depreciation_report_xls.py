# -*- coding: utf-8 -*-
# Copyright 2009-2018 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.report_xlsx_helper.report.abstract_report_xlsx \
    import AbstractReportXlsx
from odoo.exceptions import UserError
from odoo.report import report_sxw
from odoo.tools.translate import translate, _
from datetime import date as date_obj
from datetime import datetime

_logger = logging.getLogger(__name__)


IR_TRANSLATION_NAME = 'account.asset.depreciation.xlsx'
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


class AssetDepreciationReportXlsx(AbstractReportXlsx):

    def _(self, src):
        lang = self.env.context.get('lang', 'en_US')
        val = translate(
            self.env.cr, IR_TRANSLATION_NAME, 'report', lang, src) or src
        return val

    def _get_ws_params(self, wb, data, wiz):
        self.assets = self.env['account.asset'].search([('state', '!=', 'draft'),
                                                        ('type', '!=', 'view'),
                                                        ('date_start', '<=', wiz.date_to)])
        self.wiz = wiz
        s1 = self._get_depreciation_ws_params(wb, data, wiz)
        self.total_purchase_value = 0
        self.total_depreciation_base = 0
        self.total_accumulated_depreciation = 0
        self.total_month_depreciation = 0
        self.total_ytd_depreciation = 0
        return [s1]

    def _get_asset_template(self):

        asset_template = {
            'sys_no': {
                'header': {
                    'type': 'string',
                    'value': self._('Sys. No'),
                },
                'asset': {
                    'type': 'string',
                    'value': self._render(
                        "asset.sys_no"),
                },
                'totals': {
                    'type': 'string',
                    'value': self._('Totals'),
                },
                'width': 20,
            },
            'date_start': {
                'header': {
                    'type': 'string',
                    'value': self._('In Svc Date'),
                },
                'asset': {
                    'value': self._render(
                        "asset.date_start and "
                        "datetime.strptime(asset.date_start,'%Y-%m-%d') "
                        "or None"),
                    'format': self.format_tcell_date_left,
                },
                'width': 40,
            },
            'purchase_value': {
                'header': {
                    'type': 'string',
                    'value': self._('Acquired Value'),
                },
                'asset': {
                    'type': 'number',
                    'value': self._render("asset.purchase_value or 0"),
                },
                'totals': {
                    'type': 'number',
                    'value': self._render("total_purchase_value"),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 18,
            },
            'method_number': {
                'header': {
                    'type': 'string',
                    'value': self._('Years'),
                },
                'asset': {
                    'type': 'number',
                    'value': self._render("asset.method_number or 0"),
                },
                'width': 20,
            },
            'method_number_month': {
                'header': {
                    'type': 'string',
                    'value': self._('Months'),
                },
                'asset': {
                    'type': 'number',
                    'value': self._render("asset.method_number_month or 0"),
                },
                'width': 20,
            },
            'salvage_value': {
                'header': {
                    'type': 'string',
                    'value': self._('Salvage Value'),
                },
                'asset': {
                    'type': 'number',
                    'value': self._render("asset.salvage_value or 0"),
                },
                'width': 20,
            },
            'date_start': {
                'header': {
                    'type': 'string',
                    'value': self._('Asset Start Date'),
                },
                'asset': {
                    'value': self._render(
                        "asset.date_start and "
                        "datetime.strptime(asset.date_start,'%Y-%m-%d') "
                        "or None"),
                    'format': self.format_tcell_date_left,
                },
                'width': 20,
            },
            'depreciation_base': {
                'header': {
                    'type': 'string',
                    'value': self._('Depreciation Base'),
                    'format': self.format_theader_yellow_right,
                },
                'asset': {
                    'type': 'number',
                    'value': self._render('asset.depreciation_base'),
                    'format': self.format_tcell_amount_right,
                },
                'totals': {
                    'type': 'number',
                    'value': self._render("total_depreciation_base"),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 18,
            },
            'depreciation_date': {
                'header': {
                    'type': 'string',
                    'value': self._('Prior Through'),
                    'format': self.format_theader_yellow_right,
                },
                'asset': {
                    'value': self._render(
                        "prior_through"),
                    'format': self.format_tcell_amount_right,
                },
                'width': 18,
            },
            'accumulated_depreciation': {
                'header': {
                    'type': 'string',
                    'value': self._('Prior Accum Depreciation'),
                    'format': self.format_theader_yellow_right,
                },
                'asset': {
                    'type': 'number',
                    'value': self._render('accumulated_depreciation'),
                    'format': self.format_tcell_amount_right,
                },
                'totals': {
                    'type': 'number',
                    'value': self._render('total_accumulated_depreciation'),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 18,
            },
            'month_depreciation': {
                'header': {
                    'type': 'string',
                    'value': self._('Depreciation this run'),
                    'format': self.format_theader_yellow_right,
                },
                'asset': {
                    'type': 'number',
                    'value': self._render('month_depreciation'),
                    'format': self.format_tcell_amount_right,
                },
                'totals': {
                    'type': 'number',
                    'value': self._render('total_month_depreciation'),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 18,
            },
            'ytd_depreciation': {
                'header': {
                    'type': 'string',
                    'value': self._('Current YTD Depreciation'),
                    'format': self.format_theader_yellow_right,
                },
                'asset': {
                    'type': 'number',
                    'value': self._render('ytd_depreciation'),
                    'format': self.format_tcell_amount_right,
                },
                'totals': {
                    'type': 'number',
                    'value': self._render('total_ytd_depreciation'),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 18,
            },
            'accumulated_depreciation': {
                'header': {
                    'type': 'string',
                    'value': self._('Current Accum Depreciation'),
                    'format': self.format_theader_yellow_right,
                },
                'asset': {
                    'type': 'number',
                    'value': self._render('accumulated_depreciation'),
                    'format': self.format_tcell_amount_right,
                },
                'totals': {
                    'type': 'number',
                    'value': self._render('total_accumulated_depreciation'),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 18,
            }
        }
        asset_template.update(
            self.env['account.asset']._xls_asset_template())

        return asset_template

    def _get_depreciation_ws_params(self, wb, data, wiz):

        depreciation_template = self._get_asset_template()
        depreciation_template.update(
            self.env['account.asset']._xls_depreciation_expense_template())
        wl_act = self.env['account.asset']._xls_depreciation_expense_fields()
        date = wiz.date_to
        date_dt = datetime.strptime(date, '%Y-%m-%d')

        return {
            'ws_name': "Depreciation Expense Report",
            'generate_ws_method': '_depreciation_expense_report',
            'title': "Depreciation Expense Report for "+str(date_dt.strftime("%B").upper()+", "+str(date_dt.year)),
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

    def _view_add(self, acq, assets):
        parent = self.assets.filtered(lambda r: acq.parent_id == r)
        if parent and parent not in assets:
            self._view_add(parent, assets)
        assets.append(acq)

    def _depreciation_expense_report(self, workbook, ws, ws_params, data, wiz):
        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers['standard'])
        ws.set_footer(self.xls_footers['standard'])

        wl_act = ws_params['wanted_list']

        self._set_column_width(ws, ws_params)

        row_pos = 0
        row_pos = self._report_title(ws, row_pos, ws_params, data, wiz)

        actives = self.env['account.asset'].search(
            [('id', 'in', self.assets.ids)],
            order='sys_no ASC')

        if not actives:
            return self._empty_report(
                ws, row_pos, ws_params, data, wiz, 'active')

        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='header',
            default_format=self.format_theader_yellow_left)

        ws.freeze_panes(row_pos, 0)

        row_pos_start = row_pos

        done = []
        a = 0
        b = 50
        #for counter in range(1, (len(actives) / 50) + 1):
        for asset in actives:
            if not asset.sys_no:
                asset.sys_no = ' '
            self.total_purchase_value += asset.purchase_value and asset.purchase_value or 0
            self.total_depreciation_base += asset.depreciation_base and asset.depreciation_base or 0
            self.total_accumulated_depreciation += asset.get_accumulated_depreciation(self.wiz.date_to) and asset.get_accumulated_depreciation(self.wiz.date_to) or 0
            self.total_month_depreciation += asset.get_month_depreciation(self.wiz.date_to) and asset.get_month_depreciation(self.wiz.date_to) or 0
            self.total_ytd_depreciation += asset.get_ytd_depreciation(self.wiz.date_to) and asset.get_ytd_depreciation(self.wiz.date_to) or 0

            row_pos = self._write_line(
                ws, row_pos, ws_params, col_specs_section='asset',
                render_space={
                    'asset': asset,
                    'prior_through': str(wiz.date_to),
                    'accumulated_depreciation': asset.get_accumulated_depreciation(wiz.date_to) and asset.get_accumulated_depreciation(wiz.date_to) or 0,
                    'ytd_depreciation': asset.get_ytd_depreciation(wiz.date_to) and asset.get_ytd_depreciation(wiz.date_to) or 0,
                    'month_depreciation': asset.get_month_depreciation(wiz.date_to) and asset.get_month_depreciation(wiz.date_to) or 0
                    },
                default_format=self.format_tcell_left)
            done.append(asset)
            #a += 50
            #b += 50
        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='totals',
            render_space={
                'total_purchase_value': self.total_purchase_value,
                'total_depreciation_base': self.total_depreciation_base,
                'total_accumulated_depreciation': self.total_accumulated_depreciation,
                'total_month_depreciation': self.total_month_depreciation,
                'total_ytd_depreciation': self.total_ytd_depreciation,
            },
            default_format=self.format_theader_yellow_left)


AssetDepreciationReportXlsx(
    'report.account.asset.depreciation.xlsx',
    'wiz.depreciation.expense.report',
    parser=report_sxw.rml_parse)
