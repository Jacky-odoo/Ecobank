from odoo import fields, models, api
from datetime import date
from odoo.exceptions import ValidationError


class InventoryAddition(models.Model):
    _name = 'inventory.addition'
    _rec_name = 'reference'
    _order = 'date desc'
    adjustment = fields.Boolean(string='Is Adjustment', default=False)
    reference = fields.Char(string='Reference', readonly=True)
    date = fields.Date(string='Date',
                       default=False,
                       states={'draft': [('readonly', False)]},
                       readonly=True)
    addition_lines_ids = fields.One2many(comodel_name='inventory.addition.line',
                                         inverse_name='addition_id',
                                         string='Items to Receive',
                                         help='Fill in the items to Receive',
                                         readonly=True,
                                         states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed')],
                             string='State',
                             readonly=True,
                             default='draft')
    note = fields.Text(string='Note',
                       readonly=True,
                       states={'draft': [('readonly', False)]})

    @api.multi
    def copy(self, default=None):
        raise ValidationError("Sorry you are not allowed to perform this operation. Error Code BYT001")

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state == 'confirm':
                raise ValidationError("You cannot delete a receipt batch that has been confirmed. Error Code BYT004")
            else:
                return super(InventoryAddition, self).unlink()

    @api.model
    def create(self, vals):
        vals['reference'] = self.env['ir.sequence'].next_by_code('inventory.in.code')
        item = super(InventoryAddition, self).create(vals)
        return item

    @api.multi
    def confirm_addition(self):
        for rec in self:
            for line in rec.addition_lines_ids:
                if line.quantity < 1:
                    raise ValidationError("You must Receive at least one quantity. Error Code INV007")
                if line.cost < 1:
                    raise ValidationError("You must enter a cost greater than 0. Error Code INV008")
                line.compute_quantity()
                line.write({'state': 'confirm'})
                line.item_id.compute_details()
            rec.write({'state': 'confirm'})