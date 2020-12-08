from odoo.osv import osv
from odoo.report import report_sxw
from datetime import datetime


class AccountAssetDetails(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(AccountAssetDetails, self).__init__(cr, uid, name, context=context)

        self.localcontext.update({
            'get_details': self.get_details,

        })
        self.context = context

    def format_date(self, date):
        date_dt = datetime.strptime(date, '%Y-%m-%d')
        return date_dt.strftime("%d").upper()+" "+date_dt.strftime("%b").upper()+", "+str(date_dt.year)

    def get_details(self, asset_id):
        result = {
            'image': asset_id.image,
            'name': asset_id.name,
            'sys_no': asset_id.sys_no,
            'code': asset_id.code,
            'serial_no': asset_id.serial_no,
            'vendor': asset_id.vendor,
            'depreciation_base': asset_id.depreciation_base,
            'value_residual': asset_id.value_residual,
            'purchase_value': asset_id.purchase_value,
            'salvage_value': asset_id.salvage_value,
            'acquired_date': self.format_date(asset_id.acquired_date),
            'date_start': self.format_date(asset_id.date_start),
            'profile': asset_id.profile_id.name,
            'sub_category': asset_id.sub_category_id.name,
            'location': asset_id.location_id.name,
            'asset_department': asset_id.asset_department_id.name,
            'asset_unit': asset_id.asset_unit_id.name,
            'partner': asset_id.partner_id.name,
            'method_number': asset_id.method_number,
            'method_number_month': asset_id.method_number_month,
            'asset_gl_account': asset_id.asset_gl_account_id.code,
            'depreciation_expense_account': asset_id.depreciation_expense_account_id.code,
            'accumulated_depreciation_account': asset_id.accumulated_depreciation_account_id.code,
        }

        return result


class WrappedReportAureolNassitReport(osv.AbstractModel):
    _name = 'report.account_asset_management.asset_details_report_template'
    _inherit = 'report.abstract_report'
    _template = 'account_asset_management.asset_details_report_template'
    _wrapped_report_class = AccountAssetDetails
