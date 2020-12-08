from odoo import models, api, fields
from odoo.exceptions import ValidationError


class InventoryDepartment(models.Model):
    _name = 'inventory.department'
    name = fields.Char(string='Name', required=True)

    @api.multi
    def copy(self, default=None):
        raise ValidationError("Sorry you are not allowed to perform this operation. BYT001")

    @api.constrains('name')
    def check_name(self):
        all_departments = self.search([])
        for department in all_departments:
            if self.name.lower() == department.name.lower() and self.id != department.id:
                raise ValidationError("Error! Department already exist. BYT005")
