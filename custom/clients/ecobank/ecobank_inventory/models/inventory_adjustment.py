from odoo import fields, models, api
from datetime import date
from odoo.exceptions import ValidationError


class InventoryAdjustment(models.Model):
    _name = 'inventory.adjustment'
    _rec_name = 'reference'
    _order = 'date desc'
    reference = fields.Char(string='Reference', readonly=True)
    date = fields.Date(string='Date',
                       default=date.today(),
                       readonly=True,
                       states={'draft': [('readonly', False)]})
    adjustment_lines = fields.One2many(comodel_name='inventory.adjustment.line',
                                       inverse_name='adjustment_id',
                                       string='Items',
                                       help='Items Inventory to Adjust',
                                       readonly=True,
                                       states={'draft': [('readonly', False)]})
    state = fields.Selection([('refused', 'Refused'),
                              ('draft', 'Draft'),
                              ('confirmation', 'Confirmation'),
                              ('confirm', 'Confirmed')],
                             string='State',
                             readonly=True,
                             default='draft')
    note = fields.Text(string='Note',
                       readonly=True,
                       states={'draft': [('readonly', False)]})
    total_cost = fields.Float(compute='_compute_total_cost', string='Total Inventory Value')

    @api.multi
    def copy(self, default=None):
        raise ValidationError("Sorry you are not allowed to perform this operation. Error Code BYT001")

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state == 'confirm':
                raise ValidationError("You cannot delete an adjustment that has been confirmed. Error Code BYT004")
            else:
                return super(InventoryAdjustment, self).unlink()

    @api.model
    def create(self, vals):
        vals['reference'] = self.env['ir.sequence'].next_by_code('inventory.adjustment.code')
        item = super(InventoryAdjustment, self).create(vals)
        return item

    @api.multi
    def refuse_adjustment(self):
        for rec in self:
            if not rec.adjustment_lines:
                raise fields.UserError("Please specify adjustment lines")
            rec.write({'state': 'refused'})

    @api.multi
    def set_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    def check_adjustment(self):
        for rec in self:
            for line in rec.adjustment_lines:
                if line.quantity > 0 and line.cost < 1:
                    raise fields.UserError("Please enter a cost for %s" % line.item_id.name)

    @api.multi
    def confirm_adjustment(self):
        subtraction_obj = self.env['inventory.subtraction']
        subtraction_line_obj = self.env['inventory.subtraction.line']
        addition_obj = self.env['inventory.addition']
        addition_line_obj = self.env['inventory.addition.line']
        for rec in self:
            unique_items = []
            for line in rec.adjustment_lines:
                if line.item_id not in unique_items:
                    unique_items.append(line.item_id)

            # now lets set all items to zero:
            if len(unique_items) > 0:
                subtraction_id = subtraction_obj.create(
                    {'note': rec.note, 'adjustment': True, 'date': rec.date})
                subtraction_id.write({'reference': str(subtraction_id.reference) + '-ADJ'})
                for item in unique_items:
                    inventory_additions = self.env['inventory.addition.line'].search([('quantity_remaining', '>', 0),
                                                                                      ('date', '<=', rec.date),
                                                                                      ('item_id', '=', item.id)])
                    total = sum(inventory_additions.mapped('quantity_remaining'))
                    if total > 0:
                        subtraction_line_obj.create({'item_id': item.id,
                                                     'quantity': total,
                                                     'date': rec.date,
                                                     'subtraction_id': subtraction_id.id})
                subtraction_id.request_confirmation()
                subtraction_id.confirm_subtraction()

                # lets create draft Receipt
            addition_id = addition_obj.create({'note': rec.note, 'adjustment': True, 'date': rec.date})
            addition_id.write({'reference': str(addition_id.reference)+'-ADJ'})
            for line in rec.adjustment_lines:
                # lets get unique items
                if line.quantity > 0:
                    addition_line_obj.create({'item_id': line.item_id.id,
                                              'date': rec.date,
                                              'quantity': line.quantity,
                                              'addition_id': addition_id.id,
                                              'cost': line.cost})
            # Since we've removed all items old items, now lets do the new transfer
            if addition_id:
                addition_id.confirm_addition()
                rec.write({'state': 'confirm'})

    @api.multi
    def request_confirmation(self):
        for rec in self:
            rec.check_items()
            rec.check_adjustment()
            for line in rec.adjustment_lines:
                if line.quantity < 0:
                    raise fields.UserError("Quantity cannot be less than 0 for %s" % line.item_id.name)
            rec.write({'state': 'confirmation'})

    def check_items(self):
        for rec in self:
            added = []
            if rec.adjustment_lines:
                for line in rec.adjustment_lines:
                    if line.item_id.id in added:
                        raise fields.UserError(
                                "Please add %s in one line Only " % line.item_id.name)
                    else:
                        added.append(line.item_id.id)

    def _compute_total_cost(self):
        for rec in self:
            total = 0.0
            for line in rec.adjustment_lines:
                total += line.cost*line.quantity
            rec.total_cost = total
