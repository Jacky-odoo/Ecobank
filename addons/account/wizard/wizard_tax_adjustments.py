# -*- coding: utf-8 -*-
# Part of Byte. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class TaxAdjustments(models.TransientModel):
    _name = 'tax.adjustments.wizard'
    _description = 'Wizard for Tax Adjustments'

    @api.multi
    def _get_default_journal(self):
        return self.env['account.journal'].search([('type', '=', 'general')], limit=1).id

    reason = fields.Char(string='Justification', required=True)
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, default=_get_default_journal, domain=[('type', '=', 'general')])
    date = fields.Date(required=True, default=fields.Date.context_today)
    debit_account_id = fields.Many2one('account.account', string='Debit account', required=True, domain=[('deprecated', '=', False)])
    credit_account_id = fields.Many2one('account.account', string='Credit account', required=True, domain=[('deprecated', '=', False)])
    amount = fields.Monetary(currency_field='company_currency_id', required=True)
    company_currency_id = fields.Many2one('res.currency', readonly=True, default=lambda self: self.env.user.company_id.currency_id)
    tax_id = fields.Many2one('account.tax', string='Adjustment Tax', ondelete='restrict', domain=[('type_tax_use', '=', 'none'), ('tax_adjustment', '=', True)], required=True)

    @api.multi
    def _create_move(self):
        debit_vals = {
            'name': self.reason,
            'debit': self.amount,
            'credit': 0.0,
            'account_id': self.debit_account_id.id,
            'tax_line_id': self.tax_id.id,
        }
        credit_vals = {
            'name': self.reason,
            'debit': 0.0,
            'credit': self.amount,
            'account_id': self.credit_account_id.id,
            'tax_line_id': self.tax_id.id,
        }
        vals = {
            'journal_id': self.journal_id.id,
            'date': self.date,
            'state': 'draft',
            'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
        }
        move = self.env['account.move'].create(vals)
        move.post()
        return move.id

    @api.multi
    def create_move(self):
        #create the adjustment move
        move_id = self._create_move()
        #return an action showing the created move
        action = self.env.ref(self.env.context.get('action', 'account.action_move_line_form'))
        result = action.read()[0]
        result['views'] = [(False, 'form')]
        result['res_id'] = move_id
        return result
