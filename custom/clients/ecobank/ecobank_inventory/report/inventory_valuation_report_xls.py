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


IR_TRANSLATION_NAME = 'inventory.valuation.xlsx'
valuation_dict = {'lifo': 'Last in Cost', 'fifo': 'First in Cost', 'average': 'Weighted Average'}


class InventoryBalanceXlsx(AbstractReportXlsx):

    def _(self, src):
        lang = self.env.context.get('lang', 'en_US')
        val = translate(
            self.env.cr, IR_TRANSLATION_NAME, 'report', lang, src) or src
        return val

    def _get_ws_params(self, wb, data, wiz):
        self.items = self.env['inventory.item'].search([])
        self.wiz = wiz
        self.total_valuation = 0.0
        s1 = self._get_inventory_valuation_ws_params(wb, data, wiz)
        return [s1]

    def _get_item_template(self):

        item_template = {
            'code': {
                'header': {
                    'type': 'string',
                    'value': self._('Code'),
                },
                'item': {
                    'type': 'string',
                    'value': self._render(
                        "item.code"),
                },
                'totals': {
                    'type': 'string',
                    'value': self._('Totals'),
                },
                'width': 20,
            },
            'name': {
                'header': {
                    'type': 'string',
                    'value': self._('Description'),
                },
                'item': {
                    'type': 'string',
                    'value': self._render(
                        "item.name"),
                },
                'width': 40,
            },
            'uom_id': {
                'header': {
                    'type': 'string',
                    'value': self._('Unit of Measure'),
                },
                'item': {
                    'type': 'string',
                    'value': self._render(
                        "unit_of_measure"),
                },
                'width': 20,
            },
            'average_cost': {
                'header': {
                    'type': 'string',
                    'value': self._('Average Cost'),
                },
                'item': {
                    'type': 'number',
                    'value': self._render("average_cost"),
                },
                'width': 20,
            },
            'valuation': {
                'header': {
                    'type': 'string',
                    'value': self._('Inventory Value'),
                },
                'item': {
                    'type': 'number',
                    'value': self._render("valuation or 0"),
                },
                'totals': {
                    'type': 'number',
                    'value': self._render('total_valuation'),
                    'format': self.format_theader_yellow_amount_right,
                },
                'width': 20,
            },
            'value_method': {
                'header': {
                    'type': 'string',
                    'value': self._('Valuation Method'),
                },
                'item': {
                    'type': 'string',
                    'value': self._render("valuation_method"),
                },
                'width': 20,
            }
        }
        item_template.update( self.env['inventory.item']._xls_inventory_valuation_template())

        return item_template

    def _get_inventory_valuation_ws_params(self, wb, data, wiz):

        item_template = self._get_item_template()
        item_template.update(
            self.env['inventory.item']._xls_inventory_valuation_template())
        wl_act = self.env['inventory.item']._xls_inventory_valuation_fields()
        date = wiz.date
        date_dt = datetime.strptime(date, '%Y-%m-%d')

        return {
            'ws_name': "Inventory Valuation",
            'generate_ws_method': '_inventory_valuation_report',
            'title': "Inventory Valuation as at "+str(date_dt.strftime("%B").upper()+" "+str(date_dt.day)+", "+str(date_dt.year)),
            'wanted_list': wl_act,
            'col_specs': item_template,
        }

    def _report_title(self, ws, row_pos, ws_params, data, wiz):
        return self._write_ws_title(ws, row_pos, ws_params)

    def _inventory_valuation_report(self, workbook, ws, ws_params, data, wiz):
        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers['standard'])
        ws.set_footer(self.xls_footers['standard'])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        row_pos = self._report_title(ws, row_pos, ws_params, data, wiz)

        actives = self.env['inventory.item'].search(
            [('id', 'in', self.items.ids)],
            order='code ASC')

        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='header',
            default_format=self.format_theader_yellow_left)

        ws.freeze_panes(row_pos, 0)

        for item in actives:
            value_method = valuation_dict[item.valuation_method]
            unit_of_measure = ''
            if item.uom_id:
                unit_of_measure = item.uom_id.name
            if not item.code:
                item.code = ' '
            self.total_valuation += item.check_inventory_value(wiz.date)[-1]
            row_pos = self._write_line(
                ws, row_pos, ws_params, col_specs_section='item',
                render_space={
                    'item': item,
                    'average_cost': float(item.check_inventory_value(wiz.date)[0]),
                    'valuation': item.check_inventory_value(wiz.date)[-1],
                    'prior_through': str(wiz.date),
                    'valuation_method': value_method,
                    'unit_of_measure': unit_of_measure,
                    },
                default_format=self.format_tcell_left)
        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='totals',
            render_space={
                'total_valuation': self.total_valuation
            },
            default_format=self.format_theader_yellow_left)


InventoryBalanceXlsx(
    'report.inventory.valuation.xlsx',
    'wiz.inventory.valuation',
    parser=report_sxw.rml_parse)
