from odoo import models, fields, api


class StockWarehouseOrderpoint(models.Model):
	_inherit = 'stock.warehouse.orderpoint'

	@api.onchange('product_tmpl_id')
	def _onchange_product_tmpl_id(self):
		self.product_min_qty = self.product_tmpl_id.min_qty
		self.product_max_qty = self.product_tmpl_id.max_qty
