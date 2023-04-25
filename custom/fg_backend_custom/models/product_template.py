from odoo import models, fields


class ProductTemplate(models.Model):
	_inherit = 'product.template'

	min_qty = fields.Float('Minimum Quantity')
	max_qty = fields.Float('Maximum Quantity')
