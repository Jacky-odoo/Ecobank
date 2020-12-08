# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class AssetAssetLocationMove(models.Model):

	_name = 'account.asset.location.move'  
	_inherit = ['ir.needaction_mixin']

	name = fields.Text('Reason', required=True)
	original_location_id = fields.Many2one('account.asset.location',
									string="Original Location", store=True, required=True)
	destination_location_id = fields.Many2one('account.asset.location', string="New Location", required=True)
	asset_id = fields.Many2one('account.asset', string="Asset", required=True, domain="[('type', '=', 'normal')]")
	date = fields.Date(string="Date", default=fields.Date.today, required=True)
	state = fields.Selection([
		('draft', "Draft"),
		('done', "Confirmed"),
		('cancel', "Cancelled"),
	], default='draft')

	@api.model
	def _needaction_domain_get(self):
		domain = []
		if self.env['res.users'].has_group('account.group_account_manager'):
			domain = [('state', '=', 'draft')]
		return domain

	@api.onchange('asset_id')
	def onchange_asset_id(self):
		self.original_location_id = self.asset_id.location_id

	@api.one
	def action_draft(self):
		self.state = 'draft'

	@api.one
	def action_confirmed(self):
		self.state = 'done' 
		self.asset_id.location_id = self.destination_location_id

	@api.one
	def action_cancelled(self):
		self.state = 'cancel'   
		
	

