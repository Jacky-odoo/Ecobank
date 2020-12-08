from odoo import models, fields, api
from tempfile import NamedTemporaryFile
import csv
from odoo.exceptions import ValidationError
import logging
import os
import base64
from dateutil.relativedelta import relativedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta


_logger = logging.getLogger(__name__)
done = []


class WizardAssetTool(models.TransientModel):
    
    _name = 'wizard.asset.tool'
    _description = 'Update Assets'
    file = fields.Binary('CSV File')

    @api.multi
    def set_sys_no(self):
        assets = self.env['account.asset'].search([])
        for rec in assets:
            if rec.sys_no:
                rec.legacy_sys_no = rec.sys_no
                done.append(rec)
                _logger.info("processed "+str(len(done))+" out of "+str(len(assets)))

    @api.multi
    def set_sys_no_again(self):
        assets = self.env['account.asset'].search([])
        for rec in assets:
            if rec.legacy_sys_no:
                rec.sys_no = rec.legacy_sys_no
                done.append(rec)
                _logger.info("processed " + str(len(done)) + " out of " + str(len(assets)))

    @api.multi
    def fix_spaces_in_account_no(self):
        assets = self.env['account.asset'].search([])
        # lets check for depreciation expense accounts:
        done=[]
        for asset in assets:
            if asset.depreciation_expense_account_id:
                if asset.depreciation_expense_account_id.code.startswith(" "):
                    result = asset.depreciation_expense_account_id.code.split(" ")
                    code=""
                    for splits in result:
                        if len(splits)>3:
                            code= splits
                    # Lets check for the actuatl account
                    account = self.env['account.account'].search([('code', '=', code)])
                    if account:
                        asset.depreciation_expense_account_id = account
            done.append(asset)
            _logger.info("1st Run Processed "+str(len(done))+" Out of"+str(len(assets)))
        # lets check for accumulated depreciation expense accounts:
        done2=[]
        for asset in assets:
            if asset.accumulated_depreciation_account_id:
                if asset.accumulated_depreciation_account_id.code.startswith(" "):
                    result = asset.accumulated_depreciation_account_id.code.split(" ")
                    code = ""
                    for splits in result:
                        if len(splits) > 3:
                            code = splits
                    # Lets check for the actuatl account
                    account = self.env['account.account'].search([('code', '=', code)])
                    if account:
                        asset.accumulated_depreciation_account_id = account
                        done2.append(asset)
            _logger.info("2nd Run Processed " + str(len(done2)) + " Out of" + str(len(assets)))

    @api.multi
    def compute_depreciation(self):
        self.ensure_one()
        asset_obj = self.env['account.asset']

        data = self.file.decode('base64')
        done = []
        with NamedTemporaryFile(mode='r+b') as tempInFile:
            tempInFile.write(data)
            tempInFile.seek(0)
            del data
            rows = csv.DictReader(tempInFile.file, delimiter=',', quotechar='"')
            if 'SYS' not in rows.fieldnames:
                raise ValidationError('Error Required Column SYS not available')
            for row in rows:
                sys_no = row['SYS']
                asset = asset_obj.search([('sys_no', '=', sys_no)])
                if asset:
                    asset.compute_depreciation_board()
                    done.append(asset)

    @api.multi
    def compute_other_depreciation(self):

        asset_obj = self.env['account.asset']
        '''
        data = self.file.decode('base64')
        done = []
        with NamedTemporaryFile(mode='r+b') as tempInFile:
            tempInFile.write(data)
            tempInFile.seek(0)
            del data
            rows = csv.DictReader(tempInFile.file, delimiter=',', quotechar='"')
            if 'SYS' not in rows.fieldnames:
                raise ValidationError('Error Required Column SYS not available')
            for row in rows:
                sys_no = row['SYS']
                assets = asset_obj.search([('sys_no', '=', sys_no)])
                done.append(assets)
                '''

        to_process = asset_obj.search([('type', '=', 'normal')])
        processed = []
        for asset in to_process:
            asset.compute_depreciation_board()
            processed.append(asset)
            '''
            if asset not in done:
                depreciation_start_date = datetime.strptime(asset.date_start, '%Y-%m-%d')
                depreciation_stop_date = depreciation_start_date + \
                                         relativedelta(years=asset.method_number, months=asset.method_number_month + 1,
                                                       days=-1)
                if depreciation_stop_date > datetime.strptime('2018-08-30', '%Y-%m-%d'):
                    to_process.append(asset)
        for ass in to_process:
            ass.compute_depreciation_board()
            processed.append(ass)
            '''

    @api.multi
    def import_gl_accounts(self):
        self.ensure_one()
        asset_obj = self.env['account.asset']
        account_obj = self.env['account.account']

        data = self.file.decode('base64')
        not_found = []
        with NamedTemporaryFile(mode='r+b') as tempInFile:
            tempInFile.write(data)
            tempInFile.seek(0)
            del data
            rows = csv.DictReader(tempInFile.file, delimiter=',', quotechar='"')
            if 'SYS' not in rows.fieldnames:
                raise ValidationError('Error Required Column SYS not available')
            for row in rows:
                sys_no = row['SYS']
                gl_code = row['GL']
                asset = asset_obj.search([('sys_no', '=', sys_no)])
                gl_account = account_obj.search([('code', '=', gl_code), ('is_asset_gl',  '=', True)], limit=1)
                if gl_account and asset:
                    asset.asset_gl_account_id = gl_account
                else:
                    not_found.append(gl_code)
        if len(not_found) > 0:
            for item in not_found:
                msg = 'Import Not Successful ' \
                      'GLs are not found in the system.' \
                      ' These are the GLS(s) : \n'
                msg += 'Code: "%s" Name: %s \n' % (
                    item, item
                )
            raise ValidationError(msg)
