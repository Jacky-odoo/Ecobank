import time
from odoo import models, api


class AssetReport(models.AbstractModel):
    _name = 'report.asset_report.asset_asset_report'

    @api.multi
    def render_html(self, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.ids)
        docargs = {
            'doc_ids': self.ids,
            'doc_model': model,
            'data': data,
            'docs': docs,
            'time': time,
        }
        return self.env['report'].render('asset_report.asset_asset_report_template', docargs)
