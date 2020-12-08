from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import date


class InventoryAdjustmentLine(models.Model):
    _name = 'inventory.adjustment.line'
    item_id = fields.Many2one(comodel_name='inventory.item',
                              string='Item Description/Code',
                              required=True,
                              ondelete='restrict',)
    quantity = fields.Integer(string='Quantity',
                              required=True,)
    adjustment_id = fields.Many2one(comodel_name='inventory.adjustment',
                                    string='Batch',
                                    required=True,
                                    ondelete='restrict',
                                    readonly=True)
    cost = fields.Float(string='Unit Cost',
                        # related='item_id.value',
                        compute='compute_cost',
                        store=True)

    @api.onchange('item_id')
    @api.depends('item_id')
    def compute_cost(self):
        for rec in self:
            avg_cost = rec.item_id.average_cost
            if avg_cost > 0:
                rec.cost = avg_cost

