
from datetime import date
import calendar

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_CALENDER_MONTHS = (
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
)


class WizardPrintAssetReport(models.TransientModel):
    _name = 'print.asset.report'
    _description = 'Print Asset Report'

    def _current_month(self):
        return date.today().month

    month = fields.Selection(
        _CALENDER_MONTHS,
        default=_current_month
    )
    date_from = fields.Date(
        'From Date',
        required=True,
    )
    date_to = fields.Date(
        'To Date',
        required=True,
    )

    @api.onchange('month')
    @api.one
    def onchange_month(self):
        if self.month:
            year = date.today().year
            weekday, end_date = calendar.monthrange(year, self.month)
            self.date_from = date(year, self.month, 1)
            self.date_to = date(year, self.month, end_date)

    def get_assets(self):
        return []

    """
    def _get_issue_stats(self):
        issue_data = []
        issue_categories = []
        issue_categories_header = [['DRIVER']]
        driver_ids = []
        if self.issue_category_ids:
            for category in self.issue_category_ids:
                issue_categories.append({'name': category.name, 'id': category.id, })
                issue_categories_header.append([category.name])
            issue_categories_header.append(['TOTAL'])
            issue_data.append(issue_categories_header)
        if not self.issue_category_ids:
            for category in self.env['fleet.vehicle.issue.category'].search([]):
                issue_categories.append({'name': category.name, 'id': category.id, })
                issue_categories_header.append([category.name])
            issue_categories_header.append(['TOTAL'])
            issue_data.append(issue_categories_header)
        if self.driver_ids:
            for driver in self.driver_ids:
                total_issues = 0
                driver_dict = []
                driver_dict.append([driver.name])
                for cat in issue_categories:
                    issue_count = self.env['fleet.vehicle.issue'].\
                        search_count([('driver_id', '=', driver.id),
                                      ('category_id', '=', cat['id']),
                                      ('date', '>=', self.date_from),
                                      ('date', '<=', self.date_to)])
                    total_issues += issue_count
                    driver_dict.append([issue_count])
                driver_dict.append([total_issues])
                driver_ids.append(driver_dict)
            issue_data.append(driver_ids)
        if not self.driver_ids:
            for driver in self.env['fleet.driver'].search([('active', '=', True)]):
                total_issues = 0
                driver_dict = []
                driver_dict.append([driver.name])
                for cat in issue_categories:
                    issue_count = self.env['fleet.vehicle.issue'].\
                        search_count([('driver_id', '=', driver.id),
                                      ('category_id', '=', cat['id']),
                                      ('date', '>=', self.date_from),
                                      ('date', '<=', self.date_to)])
                    total_issues += issue_count
                    driver_dict.append([issue_count])
                driver_dict.append([total_issues])
                driver_ids.append(driver_dict)
            issue_data.append(driver_ids)
        return issue_data
        """

    @api.multi
    def print_report(self):
        self.ensure_one()

        asset_data = self.get_assets()

        report_obj = self.env['report'].with_context(
            active_ids=[self.id, ],
            active_model='print.asset.report'
        )
        datas = {
            'ids': [self.id, ],
            'model': 'print.asset.report',
            'form': {
                'issue_data': asset_data or [],
                'date_from': self.date_from,
                'date_to': self.date_to,
                'date': "Driver Issue Report for "+str(self.date_from)+" to "+self.date_to
            }
        }
        return report_obj.get_action(
            self,
            'asset_report.asset_asset_report',
            data=datas
        )

    @api.constrains('date_from', 'date_to')
    @api.one
    def _check_date(self):
        if self.date_from > self.date_to:
            raise ValidationError('Date from can not be greater than date to')
