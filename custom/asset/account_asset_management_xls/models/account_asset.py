# -*- coding: utf-8 -*-
# Copyright 2009-2018 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, models, fields
from odoo.addons.report_xlsx_helpers.report.abstract_report_xlsx import AbstractReportXlsx
from datetime import date as date_obj
_render = AbstractReportXlsx._render



class AccountAsset(models.Model):
    _inherit = 'account.asset'

    @api.model
    def _xls_acquisition_fields(self):
        """
        Update list in custom module to add/drop columns or change order
        """
        return [
            'account', 'name', 'code', 'date_start', 'depreciation_base',
            'salvage_value',
        ]

    @api.model
    def _xls_depreciation_expense_fields(self):
        """
        Update list in custom module to add/drop columns or change order
        """
        return [
            'sys_no', 'date_start', 'purchase_value', 'method_number', 'method_number_month',
            'salvage_value', 'depreciation_base', 'depreciation_date', 'accumulated_depreciation', 'month_depreciation',
            'ytd_depreciation', 'accumulated_depreciation',
        ]

    @api.model
    def _xls_asset_register_fields(self):
        """
        Update list in custom module to add/drop columns or change order
        """
        return [
            'sys_no','code', 'profile_id', 'sub_category_id', 'location_id',
            'name', 'method_number', 'method_number_month', 'acquired_date', 'date_start',  'purchase_value',
            'month_depreciation', 'ytd_depreciation', 'accumulated_depreciation', 'net_book_value',
        ]

    @api.model
    def _xls_active_fields(self):
        """
        Update list in custom module to add/drop columns or change order
        """
        return [
            'account', 'name', 'code', 'date_start',
            'depreciation_base', 'salvage_value',
            'fy_start_value', 'fy_depr', 'fy_end_value',
            'fy_end_depr',
            'method', 'method_number', 'prorata',
        ]

    @api.model
    def _xls_removal_fields(self):
        """
        Update list in custom module to add/drop columns or change order
        """
        return [
            'account', 'name', 'code', 'date_remove', 'depreciation_base',
            'salvage_value',
        ]

    @api.model
    def _xls_asset_template(self):
        """
        Template updates

        """
        return {}

    @api.model
    def _xls_acquisition_template(self):
        """
        Template updates

        """
        return {}

    @api.model
    def _xls_depreciation_expense_template(self):
        """
        Template updates

        """
        return {}

    @api.model
    def _xls_asset_register_template(self):
        """
        Template updates

        """
        return {}

    @api.model
    def _xls_active_template(self):
        """
        Template updates

        """
        return {}

    @api.model
    def _xls_removal_template(self):
        """
        Template updates

        """
        return {}
