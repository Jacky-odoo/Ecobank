from odoo import models, api, fields
from odoo.exceptions import ValidationError


class InventoryUom(models.Model):
    _name = 'inventory.uom'
    name = fields.Char(string='Name', required=True)

    @api.multi
    def copy(self, default=None):
        raise ValidationError("Sorry you are not allowed to perform this operation. Error Code BYT001")

    @api.constrains('name')
    def check_name(self):
        all_uom = self.search([])
        for uom in all_uom:
            if self.name.lower() == uom.name.lower() and self.id != uom.id:
                raise ValidationError("Sorry Unit of Measure already exist. Error Code BYT005")
