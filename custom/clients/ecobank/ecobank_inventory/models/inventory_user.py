# -*- coding: utf-8 -*-
# Copyright 2009-2017 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError


class InventoryUser(models.Model):
    _name = 'inventory.user'
    _rec_name = 'name_and_id'

    name = fields.Char(string='Name', required=True)
    empid = fields.Char(string='Employee ID', required=True)
    email = fields.Char(string='Email')
    name_and_id = fields.Char(compute='compute_name_id', store=True)
    note = fields.Text(string='Notes')

    @api.multi
    def copy(self, default=None):
        raise ValidationError("Sorry you are not allowed to perform this operation. Error Code BYT001")

    @api.constrains('email')
    def check_email(self):
        if self.email:
            if not tools.single_email_re.match(self.email):
                raise ValidationError("Invalid Email Address Entered. Error Code BYT007")

    @api.multi
    @api.depends('name', 'empid')
    def compute_name_id(self):
        for rec in self:
            if rec.empid:
                rec.name_and_id = str(rec.name + " (" + rec.empid + ")")
            else:
                rec.name_and_id = str(rec.name)
    _sql_constraints = [
        ('unique_empid', 'unique (empid)', "Employee ID Already Exist !"),
        ('unique_email', 'unique (email)', "Employee Email Already Exist !"),
    ]

    @api.multi
    def unlink(self):
        for rec in self:
            if len(rec.asset_ids) > 0:
                raise ValidationError("You cannot delete a user who has inventory request history. Error Code BYT004")
        return super(InventoryUser, self).unlink()
