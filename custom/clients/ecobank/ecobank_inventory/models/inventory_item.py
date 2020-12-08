from odoo import models, api, fields
from odoo.exceptions import ValidationError
from odoo.addons.report_xlsx_helpers.report.abstract_report_xlsx import AbstractReportXlsx

_render = AbstractReportXlsx._render


class InventoryItem(models.Model):
    _name = 'inventory.item'
    _rec_name = 'name_and_code'
    name = fields.Char(string='Description', required=True)
    code = fields.Char(string='Code', readonly=True)
    name_and_code = fields.Char(compute='compute_name_code', store=True)
    available_quantity = fields.Integer(string='Available Quantity',
                                        compute='compute_details',
                                        store=True)
    note = fields.Text(string='Note')
    value = fields.Float(string='Stock Value',
                         compute='compute_details',
                         store=True)
    uom_id = fields.Many2one(comodel_name='inventory.uom', string='Unit of Measure', ondelete='restrict')
    receipt_count = fields.Integer(string='Inventory Receipts',
                                   compute='compute_receipts',
                                   readonly=True)
    issue_count = fields.Integer(string='Inventory Issues',
                                 compute='compute_issues',
                                 readonly=True)
    inventory_receipt_ids = fields.One2many(comodel_name='inventory.addition.line',
                                            inverse_name='item_id',
                                            string='Inventory Receipts',
                                            readonly=True)
    inventory_issue_ids = fields.One2many(comodel_name='inventory.subtraction.line',
                                          inverse_name='item_id',
                                          string='Inventory Issues',
                                          readonly=True)
    re_order_qty = fields.Integer(string='Re-order Level', required=True)

    reorder = fields.Boolean(string='Reorder', compute='compute_reorder', store=True)
    valuation_method = fields.Selection([('fifo', 'First in Cost'),
                                         ('lifo', 'Last in Cost'),
                                         ('average', 'Weighted Average')],
                                        default='average',
                                        string='Valuation Method',
                                        required=True)
    removal_method = fields.Selection([('fifo', 'First in First Out'),
                                       ('lifo', 'Last in First Out')],
                                      default='fifo',
                                      string='Item Issue Method',
                                      required=True)
    average_cost = fields.Float(string='Average Cost', compute='compute_details')

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.inventory_issue_ids or rec.inventory_receipt_ids:
                raise ValidationError("Error Code INV004. You cannot delete an item with inventory moves")
        return super(InventoryItem, self).unlink()

    @api.depends('available_quantity', 'inventory_issue_ids', 'inventory_receipt_ids')
    def compute_reorder(self):
        for rec in self:
            rec.reorder = rec.available_quantity <= rec.re_order_qty

    @api.multi
    def copy(self, default=None):
        raise ValidationError("Error Code BYT002. Sorry you are not allowed to perform this operation")

    @api.constrains('re_order_qty')
    def check_reorder(self):
        for rec in self:
            if rec.receipt_count < 0:
                raise ValidationError("Error Code INV003. Reorder Quantity cannot be less than 0")

    @api.multi
    @api.depends('name', 'code')
    def compute_name_code(self):
        for rec in self:
            if rec.code:
                rec.name_and_code = str(rec.name + " (" + rec.code + ")")
            else:
                rec.name_and_code = str(rec.name)

    @api.depends('inventory_receipt_ids')
    @api.multi
    def compute_receipts(self):
        for rec in self:
            rec.receipt_count = len(rec.inventory_receipt_ids)

    @api.depends('inventory_issue_ids')
    @api.multi
    def compute_issues(self):
        for rec in self:
            rec.issue_count = len(rec.inventory_issue_ids)

    @api.multi
    @api.depends('inventory_issue_ids', 'inventory_receipt_ids', 'valuation_method')
    def compute_details(self):
        for rec in self:
            current_value = 0.0
            all_additions = self.env['inventory.addition.line'].search([('item_id', '=', rec.id),
                                                                        ('quantity_remaining', '>', 0),
                                                                        ('state', '=', 'confirm')])
            average_cost = 0.0
            if all_additions:
                sorted_receipts = sorted(all_additions, key=lambda x: x.date)
                if len(sorted_receipts) == 1:
                    average_cost = sorted_receipts[0].cost
                    current_value = average_cost * sorted_receipts[0].quantity_remaining
                elif len(sorted_receipts) == 2:
                    if rec.valuation_method == 'fifo':
                        average_cost = sorted_receipts[0].cost
                        current_value = average_cost * sum(all_additions.mapped('quantity_remaining'))
                    elif rec.valuation_method == 'lifo':
                        average_cost = sorted_receipts[-1].cost
                        current_value = average_cost * sum(all_additions.mapped('quantity_remaining'))
                    elif rec.valuation_method == 'average':
                        first_qty = sorted_receipts[0].quantity_remaining
                        first_value = sorted_receipts[0].cost
                        second_qty = sorted_receipts[-1].quantity_remaining
                        second_value = sorted_receipts[-1].cost
                        average_cost = ((first_qty * first_value) + (second_qty * second_value)) / (
                                    first_qty + second_qty)
                        current_value = average_cost * (first_qty + second_qty)
            rec.available_quantity = sum(all_additions.mapped('quantity_remaining'))
            rec.average_cost = average_cost
            rec.value = current_value

    @api.multi
    def copy(self, default=None):
        raise ValidationError("Error! Item cannot be duplicated. Error Code BYT001")

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('inventory.item.code')
        item = super(InventoryItem, self).create(vals)
        return item

    @api.model
    @api.depends('inventory_issue_ids', 'inventory_receipt_ids')
    def check_inventory_value(self, date):
        for rec in self:
            current_value = 0.0
            average_cost = 0.0
            receipts = self.env['inventory.addition.line'].search([('item_id', '=', rec.id),
                                                                   ('quantity_remaining', '>', 0),
                                                                   ('date', '<=', date),
                                                                   ('state', '=', 'confirm')])
            if len(receipts) < 1:
                return [average_cost, current_value]
            else:
                sorted_receipts = sorted(receipts, key=lambda x: x.date)
                if len(sorted_receipts) == 1:
                    average_cost = sorted_receipts[0].cost
                    current_value = average_cost * sorted_receipts[0].quantity_remaining
                elif len(sorted_receipts) == 2:
                    if rec.valuation_method == 'fifo':
                        average_cost = sorted_receipts[0].cost
                        current_value = average_cost * sum(receipts.mapped('quantity_remaining'))
                    elif rec.valuation_method == 'lifo':
                        average_cost = sorted_receipts[-1].cost
                        current_value = average_cost * sum(receipts.mapped('quantity_remaining'))
                    elif rec.valuation_method == 'average':
                        first_qty = sorted_receipts[0].quantity_remaining
                        first_value = sorted_receipts[0].cost
                        second_qty = sorted_receipts[-1].quantity_remaining
                        second_value = sorted_receipts[-1].cost
                        average_cost = ((first_qty * first_value) + (second_qty * second_value)) / (
                                    first_qty + second_qty)
                        current_value = average_cost * (first_qty + second_qty)

            issues = self.env['inventory.subtraction.line'].search([('item_id', '=', rec.id),
                                                                    ('quantity', '>', 0),
                                                                    ('date', '>', date),
                                                                    ('state', '=', 'confirm')])
            if len(issues) > 0:
                current_value += sum(issues.mapped('value'))
            return ["%0.2f" % average_cost, current_value]

    @api.model
    def _xls_inventory_balance_fields(self):
        return ['code', 'name', 'uom_id', 'available_quantity']

    @api.model
    def _xls_inventory_balance_template(self):
        return {}

    @api.model
    def _xls_inventory_valuation_fields(self):
        return ['code', 'name', 'uom_id', 'average_cost', 'valuation', 'value_method']

    @api.model
    def _xls_inventory_valuation_template(self):
        return {}

    @api.multi
    def write(self, vals):
        for item in ['name', 'uom_id', 're_order_qty', 'valuation_method']:
            if item in vals:
                if not self.env.user.has_group('ecobank_inventory.group_inventory_officer'):
                    raise ValidationError("Error Code BYT003. Sorry you are not allowed to modify this item")
        return super(InventoryItem, self).write(vals)
