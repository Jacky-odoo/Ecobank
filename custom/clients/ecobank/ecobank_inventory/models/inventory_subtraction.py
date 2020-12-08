from odoo import fields, models, api
from datetime import date
from odoo.exceptions import ValidationError


class InventorySubtraction(models.Model):
    _name = 'inventory.subtraction'
    _rec_name = 'reference'
    _order = 'date desc'
    reference = fields.Char(string='Reference',
                            readonly=True)
    date = fields.Date(string='Date',
                       default=fields.Date.today(),
                       readonly=True)
    subtraction_lines_ids = fields.One2many(comodel_name='inventory.subtraction.line',
                                            inverse_name='subtraction_id',
                                            string='Items to Issue',
                                            help='Fill in the items to issue',
                                            readonly=True,
                                            states={'draft': [('readonly', False)]})
    state = fields.Selection(
        [('refused', 'Refused'), ('draft', 'Draft'), ('confirmation', 'Confirmation'), ('confirm', 'Confirmed')],
        string='State',
        readonly=True,
        default='draft')
    note = fields.Text(string='Note',
                       readonly=True,
                       states={'draft': [('readonly', False)]})

    @api.multi
    def set_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    @api.multi
    def set_refuse(self):
        for rec in self:
            rec.write({'state': 'refused'})

    def check_issue(self):
        for rec in self:
            for line in rec.subtraction_lines_ids:
                if line.quantity < 1:
                    raise ValidationError("You must issue at least one quantity. Error Code INV005")
                if line.item_id.available_quantity < line.quantity:
                    error = "Error! you are trying to issue %s %s while quantity in store is %s Error Code INV006" % \
                            (line.quantity, line.item_id.name, line.item_id.available_quantity)
                    raise ValidationError(str(error))
                line.compute_details_check()

    @api.multi
    def request_confirmation(self):
        for rec in self:
            #rec.check_issue()
            rec.check_item_lines()
            rec.write({'state': 'confirmation'})

    @api.multi
    def copy(self, default=None):
        raise ValidationError("Sorry you are not allowed to perform this operation. BYT001")

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state == 'confirm':
                raise ValidationError("You cannot delete an issue batch that has been confirmed. BYT004")
            else:
                return super(InventorySubtraction, self).unlink()

    @api.model
    def create(self, vals):
        vals['reference'] = self.env['ir.sequence'].next_by_code('inventory.out.code')
        item = super(InventorySubtraction, self).create(vals)
        return item

    @api.multi
    def confirm_subtraction(self):
        for rec in self:
            # rec.check_issue()
            for line in rec.subtraction_lines_ids:
                line.compute_details()
                line.write({'state': 'confirm'})
                line.item_id.compute_details()
            rec.write({'state': 'confirm'})

    def check_item_lines(self):
        unique_items = []
        grouped_lines = {}
        # lets get  all unique items:
        for line in self.subtraction_lines_ids:
            if line.item_id not in unique_items:
                unique_items.append(line.item_id)
        # lets group unique line items
        for item in unique_items:
            item_lines = self.subtraction_lines_ids.filtered(lambda x: x.item_id.id == item.id)
            if item_lines:
                grouped_lines[item] = sorted(item_lines, key=lambda x: x.date)
        # lets loop through the grouped items
        for item_id in grouped_lines:
            first_item = grouped_lines[item_id][0]
            inventory_additions = self.env['inventory.addition.line'].search([('quantity_remaining', '>', 0),
                                                                              ('date', '<=', first_item.date),
                                                                              ('item_id', '=', item_id.id)])
            if not inventory_additions:
                raise ValidationError("Validation Error! "
                                      "There are no items available for %s "
                                      " Error code INV010" % item_id.name)
            total_items_count = sum([item.quantity for item in grouped_lines[item_id]])
            if inventory_additions:
                items_available = sum(inventory_additions.mapped('quantity_remaining'))
                if items_available < total_items_count:
                    raise fields.UserError("Items Available not enough for items being issued."
                                           "You are trying to Issue a total of %s %s but there's only %s available"
                                           " Error code INV011" % (total_items_count, item_id.name, items_available))
                # lets virtually subtract and see it it will be enough
            if len(inventory_additions) == 2:
                inventory_additions = sorted(inventory_additions, key=lambda x: x.date)
                first_additions = inventory_additions[0]
                second_additions = inventory_additions[-1]
                first_items = filter(lambda x: first_additions.date <= x.date < second_additions.date, grouped_lines[item_id])
                second_items = filter(lambda x: second_additions.date <= x.date < second_additions.date, grouped_lines[item_id])
                if first_items and second_items:
                    first_items_count = sum(first_items.mapped('quantity'))
                    second_items_count = sum(second_items.mapped('quantity'))
                    if sum(first_items.mapped('quantity')) < sum(first_additions.mapped('quantity_remaining')):
                        raise fields.UserError("Items Available not enough for items being issued."
                                               "You are trying to Issue a total of %s between %s and %s  "
                                               "but there were only %s available as at that time"
                                               " Error code INV011" % (
                                                   first_items_count, first_items[0].date, first_items[-1].date,
                                                   first_additions.quantity_remaining))

                    if sum(second_items.mapped('quantity')) < sum(second_additions.mapped('quantity_remaining')):
                        raise fields.UserError("Items Available not enough for items being issued."
                                               "You are trying to Issue a total of %s between %s and %s  "
                                               "but there were only %s available as at that time"
                                               " Error code INV011" % (
                                                   second_items_count, second_items[0].date, second_items[-1].date,
                                                   second_additions.quantity_remaining))