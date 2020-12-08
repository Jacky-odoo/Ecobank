# -*- coding: utf-8 -*-
# Copyright 2009-2017 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError


class InventorySupplier(models.Model):
    _name = 'inventory.supplier'
    _rec_name = 'name_and_code'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Supplier Code', readonly=True)
    address = fields.Char(string='Address')
    contact_person = fields.Char(string='Contact Person')
    contact_number = fields.Char(string='Contact Number')
    name_and_code = fields.Char(compute='compute_name_code', store=True)
    note = fields.Text(string='Notes')
    inventory_request_ids = fields.One2many(comodel_name='inventory.addition.line',
                                            inverse_name='supplier_id',
                                            string='Supply History',
                                            readonly=True)
    supply_count = fields.Integer(string='Supply Count',
                                  compute='compute_supply_count')

    @api.multi
    def copy(self, default=None):
        raise ValidationError("Sorry you are not allowed to perform this operation. Error Code BYT001")

    @api.multi
    def compute_supply_count(self):
        self.supply_count = len(self.inventory_request_ids)

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('supplier.code')
        supplier = super(InventorySupplier, self).create(vals)
        return supplier

    @api.multi
    @api.depends('name', 'code')
    def compute_name_code(self):
        for rec in self:
            if rec.code:
                rec.name_and_code = str(rec.name + " (" + rec.code + ")")
            else:
                rec.name_and_code = str(rec.name)
    _sql_constraints = [
        ('unique_code', 'unique (code)', "Vendor Code Already Exist !"),
        ('unique_email', 'unique (name)', "Vendor Already Exist !"),
    ]

    @api.multi
    def unlink(self):
        for rec in self:
            if len(rec.inventory_request_ids) > 0:
                raise ValidationError("You cannot delete a vendor who has inventory supply history. Error Code BYT004")
        return super(InventorySupplier, self).unlink()
