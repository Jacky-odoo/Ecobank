# -*- coding: utf-8 -*-
# Copyright 2009-2018 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.report_xlsx_helper.report.abstract_report_xlsx \
    import AbstractReportXlsx
from odoo import fields
from odoo.report import report_sxw
from odoo.tools.translate import translate, _
from datetime import datetime, date

_logger = logging.getLogger(__name__)


IR_TRANSLATION_NAME = 'inventory.balance.xlsx'


class InventoryBalanceXlsx(AbstractReportXlsx):

    def _(self, src):
        lang = self.env.context.get('lang', 'en_US')
        val = translate(
            self.env.cr, IR_TRANSLATION_NAME, 'report', lang, src) or src
        return val

    def _get_ws_params(self, wb, data, wiz):
        self.items = self.env['inventory.item'].search([])
        self.wiz = wiz
        s1 = self._get_inventory_balance_ws_params(wb, data, wiz)
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
            'available_quantity': {
                'header': {
                    'type': 'string',
                    'value': self._('Available Quantity'),
                },
                'item': {
                    'type': 'number',
                    'value': self._render("item.available_quantity or 0"),
                },
                'width': 20,
            }
        }
        item_template.update( self.env['inventory.item']._xls_inventory_balance_template())

        return item_template

    def _get_inventory_balance_ws_params(self, wb, data, wiz):

        item_template = self._get_item_template()
        item_template.update(
            self.env['inventory.item']._xls_inventory_balance_template())
        wl_act = self.env['inventory.item']._xls_inventory_balance_fields()
        date = wiz.date
        date_dt = datetime.strptime(date, '%Y-%m-%d')

        return {
            'ws_name': "Inventory Balance",
            'generate_ws_method': '_inventory_balance_report',
            'title': "Inventory Balance as at "+str(date_dt.strftime("%B").upper()+" "+str(date_dt.day)+", "+str(date_dt.year)),
            'wanted_list': wl_act,
            'col_specs': item_template,
        }

    def _report_title(self, ws, row_pos, ws_params, data, wiz):
        return self._write_ws_title(ws, row_pos, ws_params)

    def _inventory_balance_report(self, workbook, ws, ws_params, data, wiz):
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

        done = []
        if fields.Date.from_string(wiz.date) == date.today():
            for item in actives:
                unit_of_measure = ''
                if item.uom_id:
                    unit_of_measure = item.uom_id.name
                if not item.code:
                    item.code = ' '
                row_pos = self._write_line(
                    ws, row_pos, ws_params, col_specs_section='item',
                    render_space={
                        'item': item,
                        'available_quantity': item.available_quantity,
                        'prior_through': str(wiz.date),
                        'unit_of_measure': unit_of_measure
                        },
                    default_format=self.format_tcell_left)
                done.append(item)
        else:
            for item in actives:
                available_quantity = item.available_quantity
                removals = self.env['inventory.subtraction.line'].search([('item_id', '=', item.id),
                                                                          ('date', '>', wiz.date)])
                if len(removals) > 1:
                    available_quantity += sum(removals.mapped('quantity'))
                if not item.code:
                    item.code = ' '
                row_pos = self._write_line(
                    ws, row_pos, ws_params, col_specs_section='item',
                    render_space={
                        'item': item,
                        'available_quantity': available_quantity,
                        'prior_through': str(wiz.date),
                        },
                    default_format=self.format_tcell_left)
                done.append(item)


InventoryBalanceXlsx(
    'report.inventory.balance.xlsx',
    'wiz.inventory.balance',
    parser=report_sxw.rml_parse)
