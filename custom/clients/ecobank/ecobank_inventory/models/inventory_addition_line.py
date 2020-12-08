from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import date


class InventoryAdditionLine(models.Model):
    _name = 'inventory.addition.line'
    _rec_name = 'reference'
    reference = fields.Char(string='Reference', readonly=True)
    date = fields.Date(related='addition_id.date',
                       required=True,
                       readonly=True,
                       store=True,
                       states={'draft': [('readonly', False)]})
    item_id = fields.Many2one(comodel_name='inventory.item',
                              string='Item Description/Code',
                              required=True,
                              readonly=True,
                              ondelete='restrict',
                              states={'draft': [('readonly', False)]})
    quantity = fields.Integer(string='Quantity In',
                              required=True,
                              readonly=True,
                              states={'draft': [('readonly', False)]})
    addition_id = fields.Many2one(comodel_name='inventory.addition',
                                  string='Batch',
                                  required=True,
                                  ondelete='restrict',
                                  readonly=True)
    cost = fields.Float(string='Unit Cost',
                        required=True,
                        readonly=True,
                        states={'draft': [('readonly', False)]})
    supplier_id = fields.Many2one(comodel_name='inventory.supplier',
                                  string='Supplier',
                                  readonly=True,
                                  states={'draft': [('readonly', False)]},
                                  ondelete='restrict')
    quantity_remaining = fields.Integer(string='Remaining Qty', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed')],
                             string='State',
                             default='draft',
                             readonly=True)
    invoice_number = fields.Char(string='Inv #', required=True)

    @api.multi
    def copy(self, default=None):
        raise ValidationError("Sorry you are not allowed to perform this operation. Error Code BYT001")

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state == 'confirm':
                raise ValidationError("You cannot delete an item receipt that has been confirmed. Error Code BYT004")
            else:
                return super(InventoryAdditionLine, self).unlink()

    @api.constrains('quantity')
    def validation(self):
        count = self.search([('item_id', '=', self.item_id.id), ('quantity_remaining', '>', 0)])
        if len(count) > 1:
            raise ValidationError("You cannot have more than two "
                                  "Inventory receipt batch with remaining balances greater than 0."
                                  "Make sure you exhaust the existing balances first. Error Code INV009")

    @api.depends('item_id', 'reference')
    @api.multi
    def compute_name(self):
        for rec in self:
            if rec.item_id and rec.reference:
                rec.name = str(rec.item_id.name)+" ( "+str(rec.reference)+" )"
            else:
                rec.name = rec.reference or rec.item_id.name

    @api.depends('amount')
    def compute_quantity(self):
        for rec in self:
            if rec.item_id:
                rec.quantity_remaining = rec.quantity

    @api.model
    def create(self, vals):
        vals['reference'] = self.env['ir.sequence'].next_by_code('item.in.code')
        item = super(InventoryAdditionLine, self).create(vals)
        return item

    @api.model
    def _xls_inventory_move_receipt_fields(self):
        return ['code', 'name', 'date', 'quantity', 'supplier_id', 'batch_no', 'total']

    @api.model
    def _xls_inventory_move_receipt_template(self):
        return {}