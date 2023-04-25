from odoo import models, fields


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	state = fields.Selection(selection_add=[('to_approve', 'To Approve')])

	def action_confirm(self):
		user_has_manager = self.env.user.has_group(
			'sales_team.group_sale_manager')
		if user_has_manager:
			return super(SaleOrder, self).action_confirm()
		else:
			customer_total_amount_due = sum(
				self.env['account.move'].sudo().search([
					('state', '!=', 'cancel'),
					('move_type', '=', 'out_invoice'),
					('partner_id', '=', self.partner_id.id)]).mapped('amount_residual'))

			customer_credit_limit = self.partner_id.credit_limit

			if customer_total_amount_due > customer_credit_limit:
				self.state = 'to_approve'
				return True
			else:
				return super(SaleOrder, self).action_confirm()
