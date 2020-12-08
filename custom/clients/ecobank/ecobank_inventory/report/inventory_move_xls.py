# -*- coding: utf-8 -*-
# Copyright 2009-2018 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.report_xlsx_helper.report.abstract_report_xlsx import AbstractReportXlsx
from odoo.report import report_sxw
from odoo.tools.translate import translate, _
from datetime import datetime
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


IR_TRANSLATION_NAME = 'inventory.moves.xlsx'


class InventoryMovesXlsx(AbstractReportXlsx):

    def _(self, src):
        lang = self.env.context.get('lang', 'en_US')
        val = translate(
            self.env.cr, IR_TRANSLATION_NAME, 'report', lang, src) or src
        return val

    def _get_ws_params(self, wb, data, wiz):
        domain = [('date', '>=', wiz.date_from), ('date', '<=', wiz.date_to)]
        self.total_issue_cost = 0.0
        self.total_receipt_cost = 0.0
        self.wiz = wiz
        if wiz.move_type == 'receipt':
            self.receipt_lines = wiz.env['inventory.addition.line'].search(domain)
            if len(self.receipt_lines) < 1:
                raise ValidationError("No Move Lines to report on")
        if wiz.move_type == 'issue':
            self.issue_lines = wiz.env['inventory.subtraction.line'].search(domain)
            if len(self.issue_lines) < 1:
                raise ValidationError("No Move Lines to report on")

        if wiz.move_type == 'both':
            self.receipt_lines = wiz.env['inventory.addition.line'].search(domain)
            self.issue_lines = wiz.env['inventory.subtraction.line'].search(domain)
            if len(self.issue_lines) < 1 and len(self.receipt_lines) < 1:
                raise ValidationError("No Move Lines to report on")

        s1 = self._get_inventory_move_ws_params(wb, data, wiz)
        return [s1]

    def _get_issue_item_template(self):

        issue_item_template = {
            'code': {
                'header': {
                    'type': 'string',
                    'value': self._('Code'),
                },
                'move': {
                    'type': 'string',
                    'value': self._render(
                        "move.item_id.code"),
                },
                'width': 20,
            },
            'name': {
                'header': {
                    'type': 'string',
                    'value': self._('Description'),
                },
                'move': {
                    'type': 'string',
                    'value': self._render(
                        "move.item_id.name"),
                },
                'totals': {
                    'type': 'string',
                    'value': self._('Total'),
                },
                'width': 40,
            },
            'date': {
                'header': {
                    'type': 'string',
                    'value': self._('Move Date'),
                },
                'move': {
                    'type': 'string',
                    'value': self._render(
                        "move.date"),
                },
                'width': 20,
            },
            'quantity': {
                'header': {
                    'type': 'string',
                    'value': self._('Quantity'),
                },
                'move': {
                    'type': 'number',
                    'value': self._render("move.quantity or 0"),
                },
                'width': 20,
            },
            'total': {
                'header': {
                    'type': 'string',
                    'value': self._('Total Cost'),
                },
                'move': {
                    'type': 'number',
                    'value': self._render("total_cost or 0"),
                },
                'totals': {
                    'type': 'number',
                    'value': self._render("total_issue_cost or 0"),
                },
                'width': 20,
            },
            'branch_id': {
                'header': {
                    'type': 'string',
                    'value': self._('Branch'),
                },
                'move': {
                    'type': 'string',
                    'value': self._render("move.branch_id.name"),
                },
                'width': 20,
            }
        }
        issue_item_template.update( self.env['inventory.subtraction.line']._xls_inventory_move_issue_template())

        return issue_item_template

    def _get_receipt_item_template(self):

        receipt_item_template = {
            'code': {
                'header': {
                    'type': 'string',
                    'value': self._('Code'),
                },
                'move': {
                    'type': 'string',
                    'value': self._render(
                        "move.item_id.code"),
                },

                'totals': {
                    'type': 'string',
                    'value': self._('Total'),
                },
                'width': 20,
            },
            'name': {
                'header': {
                    'type': 'string',
                    'value': self._('Description'),
                },
                'move': {
                    'type': 'string',
                    'value': self._render(
                        "move.item_id.name"),
                },
                'width': 40,
            },
            'date': {
                'header': {
                    'type': 'string',
                    'value': self._('Move Date'),
                },
                'move': {
                    'type': 'string',
                    'value': self._render(
                        "move.date"),
                },
                'width': 20,
            },
            'quantity': {
                'header': {
                    'type': 'string',
                    'value': self._('Quantity'),
                },
                'move': {
                    'type': 'number',
                    'value': self._render("move.quantity or 0"),
                },
                'width': 20,
            },
            'total': {
                'header': {
                    'type': 'string',
                    'value': self._('Total Cost'),
                },
                'move': {
                    'type': 'number',
                    'value': self._render("total_cost or 0"),
                },
                'totals': {
                    'type': 'number',
                    'value': self._render("total_receipt_cost or 0"),
                },
                'width': 20,
            },
            'supplier_id': {
                'header': {
                    'type': 'string',
                    'value': self._('Supplier'),
                },
                'move': {
                    'type': 'string',
                    'value': self._render("move.supplier_id.name"),
                },
                'width': 20,
            },
            'batch_no': {
                'header': {
                    'type': 'string',
                    'value': self._('Batch #'),
                },
                'move': {
                    'type': 'string',
                    'value': self._render("move.addition_id.reference"),
                },
                'width': 20,
            }
        }
        receipt_item_template.update( self.env['inventory.addition.line']._xls_inventory_move_receipt_template())

        return receipt_item_template

    def _get_move_template(self):

        item_move_template = {
            'code': {
                'header': {
                    'type': 'string',
                    'value': self._('Code'),
                },
                'move': {
                    'type': 'string',
                    'value': self._render(
                        "move['code']"),
                },
                'width': 20,
            },
            'name': {
                'header': {
                    'type': 'string',
                    'value': self._('Description'),
                },
                'move': {
                    'type': 'string',
                    'value': self._render(
                        "move['name']"),
                },
                'width': 40,
            },
            'date': {
                'header': {
                    'type': 'string',
                    'value': self._('Move Date'),
                },
                'move': {
                    'type': 'string',
                    'value': self._render(
                        "move['date']"),
                },
                'width': 20,
            },
            'quantity': {
                'header': {
                    'type': 'string',
                    'value': self._('Quantity'),
                },
                'move': {
                    'type': 'number',
                    'value': self._render("move['quantity']or 0"),
                },
                'width': 20,
            },
            'value': {
                'header': {
                    'type': 'string',
                    'value': self._('Cost'),
                },
                'move': {
                    'type': 'number',
                    'value': self._render("move['value'] or 0"),
                },
                'width': 20,
            },
            'direction': {
                'header': {
                    'type': 'string',
                    'value': self._(' Move Type'),
                },
                'move': {
                    'type': 'string',
                    'value': self._render("move['direction']"),
                },
                'width': 20,
            }
        }
        item_move_template.update( self.env['inventory.subtraction.line']._xls_inventory_move_template())

        return item_move_template

    def _get_inventory_move_ws_params(self, wb, data, wiz):

        issue_item_template = self._get_issue_item_template()
        issue_item_template.update(
            self.env['inventory.subtraction.line']._xls_inventory_move_issue_template())

        receipt_item_template = self._get_receipt_item_template()
        receipt_item_template.update(
            self.env['inventory.addition.line']._xls_inventory_move_receipt_template())


        item_moves_template = self._get_move_template()
        item_moves_template.update(
            self.env['inventory.subtraction.line']._xls_inventory_move_template())


        moves_wl_act = self.env['inventory.subtraction.line']._xls_inventory_move_fields()
        issue_wl_act = self.env['inventory.subtraction.line']._xls_inventory_move_issue_fields()
        receipt_wl_act = self.env['inventory.addition.line']._xls_inventory_move_receipt_fields()
        date_from = wiz.date_from
        date_to = wiz.date_to
        date_from_dt = datetime.strptime(date_from, '%Y-%m-%d')
        date_to_dt = datetime.strptime(date_to, '%Y-%m-%d')

        if self.wiz.move_type == 'issue':

            return {
                'ws_name': "Inventory Issue",
                'generate_ws_method': '_inventory_issue_report',
                'title': "Inventory Issue from "+str(date_from_dt.strftime("%B").upper()+" "+str(date_from_dt.day)+", "+str(date_from_dt.year))+" to "+str(date_to_dt.strftime("%B").upper()+" "+str(date_to_dt.day)+", "+str(date_to_dt.year)),
                'wanted_list': issue_wl_act,
                'col_specs': issue_item_template,
            }
        elif self.wiz.move_type == 'receipt':
            return {
                'ws_name': "Inventory Receipt",
                'generate_ws_method': '_inventory_receipt_report',
                'title': "Inventory Receipt from "+str(date_from_dt.strftime("%B").upper()+" "+str(date_from_dt.day)+", "+str(date_from_dt.year))+" to "+str(date_to_dt.strftime("%B").upper()+" "+str(date_to_dt.day)+", "+str(date_to_dt.year)),
                'wanted_list': receipt_wl_act,
                'col_specs': receipt_item_template,
            }

        elif self.wiz.move_type == 'both':
            return {
                'ws_name': "Inventory Moves",
                'generate_ws_method': '_inventory_move_report',
                'title': "Inventory Moves from "+str(date_from_dt.strftime("%B").upper()+" "+str(date_from_dt.day)+", "+str(date_from_dt.year))+" to "+str(date_to_dt.strftime("%B").upper()+" "+str(date_to_dt.day)+", "+str(date_to_dt.year)),
                'wanted_list': moves_wl_act,
                'col_specs': item_moves_template,
            }

    def _report_title(self, ws, row_pos, ws_params, data, wiz):
        return self._write_ws_title(ws, row_pos, ws_params)

    def _inventory_receipt_report(self, workbook, ws, ws_params, data, wiz):
        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers['standard'])
        ws.set_footer(self.xls_footers['standard'])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        row_pos = self._report_title(ws, row_pos, ws_params, data, wiz)

        actives = self.env['inventory.addition.line'].search(
            [('id', 'in', self.receipt_lines.ids)])

        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='header',
            default_format=self.format_theader_yellow_left)

        ws.freeze_panes(row_pos, 0)

        done = []
        for move in actives:
            total_cost = move.cost*move.quantity
            self.total_receipt_cost += total_cost
            row_pos = self._write_line(
                ws, row_pos, ws_params, col_specs_section='move',
                render_space={
                    'move': move,
                    'total_cost': total_cost
                    },
                default_format=self.format_tcell_left)
            done.append(move)
        self._write_line(
            ws, row_pos, ws_params, col_specs_section='totals',
            render_space={
                'total_receipt_cost': self.total_receipt_cost
            },
            default_format=self.format_theader_yellow_left)

    def _inventory_issue_report(self, workbook, ws, ws_params, data, wiz):
        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers['standard'])
        ws.set_footer(self.xls_footers['standard'])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        row_pos = self._report_title(ws, row_pos, ws_params, data, wiz)

        actives = self.env['inventory.subtraction.line'].search(
            [('id', 'in', self.issue_lines.ids)])

        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='header',
            default_format=self.format_theader_yellow_left)

        ws.freeze_panes(row_pos, 0)

        done = []
        for move in actives:
            self.total_issue_cost += move.value
            row_pos = self._write_line(
                ws, row_pos, ws_params, col_specs_section='move',
                render_space={
                    'move': move,
                    'total_cost': move.value
                    },
                default_format=self.format_tcell_left)
            done.append(move)
        self._write_line(
            ws, row_pos, ws_params, col_specs_section='totals',
            render_space={
                'total_issue_cost': self.total_issue_cost
            },
            default_format=self.format_theader_yellow_left)

    def _inventory_move_report(self, workbook, ws, ws_params, data, wiz):
        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers['standard'])
        ws.set_footer(self.xls_footers['standard'])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        row_pos = self._report_title(ws, row_pos, ws_params, data, wiz)

        active_issues = self.env['inventory.subtraction.line'].search(
            [('id', 'in', self.issue_lines.ids)])

        active_receipts = self.env['inventory.addition.line'].search(
            [('id', 'in', self.receipt_lines.ids)])

        all_moves = []
        for line in active_issues:
            all_moves.append(({'code': line.item_id.code,
                               'name': line.item_id.name,
                               'direction': 'Issue',
                               'date': line.date,
                               'quantity': line.quantity,
                               'value': line.value}))

        for line in active_receipts:
            all_moves.append(({'code': line.item_id.code,
                               'name': line.item_id.name,
                               'direction': 'Receipt',
                               'date': line.date,
                               'quantity': line.quantity,
                               'value': line.cost}))
        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='header',
            default_format=self.format_theader_yellow_left)

        ws.freeze_panes(row_pos, 0)

        done = []
        for move in all_moves:
            row_pos = self._write_line(
                ws, row_pos, ws_params, col_specs_section='move',
                render_space={
                    'move': move
                    },
                default_format=self.format_tcell_left)
            done.append(move)


InventoryMovesXlsx(
    'report.inventory.moves.xlsx',
    'wiz.inventory.move',
    parser=report_sxw.rml_parse)
