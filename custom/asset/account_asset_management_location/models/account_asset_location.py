# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo import tools


class AccountAssetLocation(models.Model):

    _name = 'account.asset.location'
    _sql_constraints = [('name_unique', 'unique(name)', 'Asset Location must be Unique!'),
                        ('code_unique', 'unique(code)', 'Asset Location Code must be Unique!')]

    @api.one 
    @api.depends('name', 'parent_id')
    def _loc_name_get_fnc(self):
        name = self.name
        if self.parent_id:
            name = self.parent_id.display_name + ' / ' + name
        self.display_name = name
    
    name = fields.Char('Location', required=True) 
    parent_id = fields.Many2one('account.asset.location','Parent Location')
    display_name = fields.Char(compute='_loc_name_get_fnc',string='Name', 
                            store=True, readonly=True)    
    child_ids = fields.One2many('account.asset.location', 'parent_id', 
                            'Child Location') 

    @api.multi 
    def name_get(self):
        result = []
        for location in self: 
            result.append((location.id, location.display_name))
        return result 

    @api.constrains('parent_id')
    @api.multi
    def _check_recursion(self):
        level = 100
        cr = self.env.cr
        while len(self.ids):
            cr.execute('select distinct parent_id from account_asset_location where id IN %s',
                (tuple(self.ids),))
            ids = filter(None, map(lambda x: x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True
