from datetime import datetime, timedelta
from odoo import api, models


class AssetDetailsReport(models.AbstractModel):
    _name = 'report.account_asset_ecobank_customization.asset_report'

    def get_cat_id(self, tag_id):
        tages = ''
        if tag_id:
            for tage in tag_id:
                tages += tage.name +','
        return tages
        
    @api.model
    def render_html(self, docids, data=None):
        asset = self.env['account.asset'].browse(docids)
        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.asset',
            'docs': asset,
            'data': data,
            'get_cat_id': self.get_cat_id,
        }
        return self.env['report'].render('account_asset_ecobank_customization.asset_details_report_template', docargs)
