from odoo import fields, models, api
from odoo.exceptions import ValidationError


class InventorySubtractionLine(models.Model):
    _name = 'inventory.subtraction.line'
    _rec_name = 'name'
    name = fields.Char(compute='compute_name', string='Name', store=True)
    reference = fields.Char(string='Reference')
    date = fields.Date(string='Date', required=True)
    item_id = fields.Many2one(comodel_name='inventory.item',
                              string='Item Description/Code',
                              ondelete='restrict',
                              domain="[('available_quantity','>',0)]",
                              required=True)
    quantity = fields.Integer(string='Qty Out', required=True)
    subtraction_id = fields.Many2one(comodel_name='inventory.subtraction',
                                     ondelete='cascade',
                                     required=True,
                                     readonly=True)
    value = fields.Float(string='Value', compute='compute_value', readonly=True, store=True)
    branch_id = fields.Many2one(comodel_name='inventory.branch',
                                string='Branch',
                                ondelete='restrict',
                                help='Select the branch requesting')
    department_id = fields.Many2one(comodel_name='inventory.department',
                                    string='Department',
                                    help='Select the branch requesting if available',
                                    ondelete='restrict')
    issuer = fields.Char(comodel_name='inventory.user',
                         string='Issued By',
                         help='Enter Name the person issuing the items')
    recipient = fields.Char(comodel_name='inventory.user',
                            string='Received By',
                            help='Enter the name of the person receiving the item(s)')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed')],
                             string='State',
                             default='draft',
                             readonly=True)

    @api.multi
    def copy(self, default=None):
        raise ValidationError("Sorry you are not allowed to perform this operation. Error Code BYT001")

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state == 'confirm':
                raise ValidationError("You cannot delete an item issue that has been confirmed. INV004")
            else:
                return super(InventorySubtractionLine, self).unlink()

    @api.depends('item_id', 'reference')
    @api.multi
    def compute_name(self):
        for rec in self:
            if rec.item_id and rec.reference:
                rec.name = str(rec.item_id.name) + " ( " + str(rec.reference) + " )"
            else:
                rec.name = rec.reference or rec.item_id.name

    @api.depends('quantity')
    def compute_value(self):
        for rec in self:
            value = 0.0
            amount = rec.quantity
            if rec.item_id:
                # lets get previous addition lines
                inventory_additions = self.env['inventory.addition.line'].search([('quantity_remaining', '>', 0),
                                                                                  ('date', '<=', rec.date),
                                                                                  ('item_id', '=', rec.item_id.id)])
                if not inventory_additions:
                    raise ValidationError("Validation Error! Date Mismatch! "
                                          "There were no items available for %s as at the date %s you specified "
                                          " Error code INV001" % (rec.item_id.name, rec.date))
                if len(inventory_additions) > 0:
                    if len(inventory_additions) == 1:
                        for line in inventory_additions:
                            if line.date > rec.date:
                                raise ValidationError("Validation Error! Date Mismatch! "
                                                      "There were no items available for %s as at the date %s you specified "
                                                      " Error code INV001" % (rec.item_id.name, rec.date))

                    if len(inventory_additions) > 1:
                        flag = False

                        for line in inventory_additions:
                            if line.date > rec.date:
                                flag = True
                        if flag:
                            raise ValidationError("Validation Error! Date Mismatch! "
                                                  "There were no items available for %s as at the date %s you specified "
                                                  " Error code INV001" % (rec.item_id.name, rec.date))
                    if rec.item_id.removal_method == 'fifo':
                        lines = sorted(inventory_additions, key=lambda x: x.date)
                    else:
                        lines = sorted(inventory_additions, key=lambda x: x.date, reverse=True)
                    if rec.quantity > sum(inventory_additions.mapped('quantity_remaining')):
                        raise ValidationError(
                            'Error code INV002. There is not enough items left for ' + str(rec.item_id.name) +
                            ' Total Remaining Balance for ' + str(rec.item_id.name) + ' is ' +
                            str(sum(inventory_additions.mapped('quantity_remaining'))))
                    else:
                        while amount > 0:
                            for addition in lines:
                                if addition.quantity_remaining >= amount:
                                    value += amount * addition.cost
                                    amount = 0
                                elif amount > addition.quantity_remaining >= 0:
                                    value += (addition.quantity_remaining * addition.cost)
                                    amount = amount - addition.quantity_remaining
            rec.value = value

    def compute_details_check(self):
        for rec in self:
            if rec.item_id:
                # lets get previous addition lines
                inventory_additions = self.env['inventory.addition.line'].search([('quantity_remaining', '>', 0),
                                                                                  ('item_id', '=', rec.item_id.id)])

                if not inventory_additions:
                    raise ValidationError("Validation Error! Date Mismatch! "
                                          "There were no items available for %s as at the date %s you specified "
                                          " Error code INV001" % (rec.item_id.name, rec.date))

                if len(inventory_additions) > 0:
                    flag = False
                    if len(inventory_additions) == 1:
                        for line in inventory_additions:
                            if line.date > rec.date:
                                flag = True
                        if flag:
                            raise ValidationError("Validation Error! Date Mismatch! "
                                                  "There were no items available for %s as at the date %s you specified "
                                                  " Error code INV001" % (rec.item_id.name, rec.date))
                    if len(inventory_additions) > 1:
                        flag = False
                        for line in inventory_additions:
                            if line.quantity_remaining >= rec.quantity:
                                flag = False
                                continue
                            if line.date > rec.date:
                                flag = True
                        if flag:
                            raise ValidationError("Validation Error! Date Mismatch! "
                                                  "There were no items available for %s as at the date %s you specified "
                                                  " Error code INV001" % (rec.item_id.name, rec.date))
                    if rec.quantity > sum(inventory_additions.mapped('quantity_remaining')):
                        raise ValidationError(
                            'Error code INV002. There is not enough items left for ' + str(rec.item_id.name) +
                            ' Total Remaining Balance for ' + str(rec.item_id.name) + ' is ' +
                            str(sum(inventory_additions.mapped('quantity_remaining'))))

    def compute_details(self):
        for rec in self:
            value = 0.0
            amount = rec.quantity
            if rec.item_id:
                # lets get previous addition lines
                inventory_additions = self.env['inventory.addition.line'].search([('quantity_remaining', '>', 0),
                                                                                  ('item_id', '=', rec.item_id.id)])
                lines = sorted(inventory_additions, key=lambda x: x.date)
                if rec.quantity > sum(inventory_additions.mapped('quantity_remaining')):
                    raise ValidationError(
                        'Error code INV002. There is not enough items left for ' + str(rec.item_id.name) +
                        ' Total Remaining Balance for ' + str(rec.item_id.name) + ' is ' +
                        str(sum(inventory_additions.mapped('quantity_remaining'))))
                else:
                    while amount > 0:
                        for addition in lines:
                            if addition.quantity_remaining >= amount:
                                value += amount * addition.cost
                                addition.quantity_remaining = addition.quantity_remaining - amount
                                amount = 0
                            elif amount > addition.quantity_remaining >= 0:
                                value += (addition.quantity_remaining * addition.cost)
                                amount = amount - addition.quantity_remaining
                                addition.quantity_remaining = 0
        rec.value = value

    @api.model
    def create(self, vals):
        vals['reference'] = self.env['ir.sequence'].next_by_code('item.out.code')
        item = super(InventorySubtractionLine, self).create(vals)
        return item

    @api.model
    def _xls_inventory_move_issue_fields(self):
        return ['name', 'code', 'date', 'quantity', 'total', 'branch_id']

    @api.model
    def _xls_inventory_move_issue_template(self):
        return {}

    @api.model
    def _xls_inventory_move_fields(self):
        return ['name', 'code', 'date', 'quantity', 'value', 'direction']

    @api.model
    def _xls_inventory_move_template(self):
        return {}
