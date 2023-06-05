from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('to_approve', 'To Approve')])

    def action_confirm(self):
        """
        Method Over-ride : For additional functionality added to restrict particular customer sale order with credit-limit
        :return: "To Approve" while customer credit limit reached otherwise directly "confirm" the sale order for user doesn't have administrator rights.
        """

        user_has_manager = self.env.user.has_group(
            'sales_team.group_sale_manager')
        if user_has_manager:
            return super(SaleOrder, self).action_confirm()
        else:
            customer_total_amount_in_so = sum(self.env['sale.order'].sudo().search(
                [('state', 'in', ['sale', 'to_approve']),
                 ('partner_id', '=', self.partner_id.id)]).mapped('amount_total'))

            customer_total_amount_due_in_invoice = sum(
                self.env['account.move'].sudo().search([
                    ('payment_state', '=', 'paid'),
                    ('move_type', '=', 'out_invoice'),
                    ('partner_id', '=', self.partner_id.id)]).mapped('amount_total'))

            total_amount_to_restrict = (
                                               customer_total_amount_in_so + self.amount_total) - customer_total_amount_due_in_invoice
            print("-----customer_total_amount_in_so----------", customer_total_amount_in_so)
            print("-----customer_total_amount_due_in_invoice----------", customer_total_amount_due_in_invoice)
            print("-----total_amount_to_restrict----------", total_amount_to_restrict)
            customer_credit_limit = self.partner_id.credit_limit
            if total_amount_to_restrict > customer_credit_limit:
                self.state = 'to_approve'
                return True
            else:
                return super(SaleOrder, self).action_confirm()
