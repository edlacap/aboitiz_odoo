# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class FgPosReport(models.AbstractModel):
    _name = 'report.fg_custom.report_fg_pos_report'
    _description = 'POS Report'

    def action_print(self, data):

        headers = 'SI#,Order Date,Total Items,Total Amount,Vat Exempt, Vat Zero-Rated, Vatable,VAT,PWD/SC Discount,PWD/SC Discount Amount,Other Discount,Total Amount Paid'  #will change depends on report type, by default, daily sales report
        order_report = []
        run_report_date = datetime.today().strftime('%Y-%m-%d')

        company = self.env.company

        if data.get('report_type') == 'daily_sales':
            orders = self.env['pos.order'].search([('pos_si_trans_reference', '!=', False), ('date_order', '>=', data.get('date_start')),('date_order', '<=', data.get('date_stop'))])
            report_type = 'Daily Sales'
        elif data.get('report_type') == 'refund_report':
            orders = self.env['pos.order'].search([('pos_refund_si_reference', '!=', False), ('date_order', '>=', data.get('date_start')), ('date_order', '<=', data.get('date_stop'))])
            report_type = 'Refund Report'
            headers = 'Refund SI#,Reference SI#,Refund Date,Total Items,Total Amount,Vat Exempt, Vat Zero-Rated, Vatable,VAT,PWD/SC Discount,PWD/SC Discount Amount,Other Discount,Total Amount Paid'  # will change depends on report type, by default, daily sales report

        for order in orders:
            #get computed values in order lines
            line_computed_values = order._get_lines_computed_values(order)

            refNumber = None #refund/si reference
            siReferenceNumber = None #si reference or refunded order
            if report_type == 'Daily Sales':
                refNumber = order.pos_si_trans_reference
            elif report_type == 'Refund Report':
                refNumber = order.pos_refund_si_reference
                siReferenceNumber = order.pos_refunded_id.pos_si_trans_reference

            #amount_tax,  amount total, amount_paid
            order_report.append({'refNum': refNumber, 'reference_si': siReferenceNumber, 'date_order' : order.date_order.strftime('%Y-%m-%d %H:%M:%S'),'vat': order.amount_tax, 'amount_paid': order.amount_paid,
                                 'total_discount': line_computed_values.get('total_discount'), 'total_product_v': line_computed_values.get('total_product_v'),
                                 'total_vat': line_computed_values.get('total_vat'),'total_product_e': line_computed_values.get('total_product_e'),
                                 'total_qty': line_computed_values.get('total_qty'),'government_discount_name': line_computed_values.get('government_discount_name'),
                                 'government_total_discount': line_computed_values.get('government_total_discount'), 'total_amount': line_computed_values.get('total_amount'),
                                 'total_product_z': line_computed_values.get('total_product_z')
                                 })

        returndata = {
            'report_type': report_type,
            'run_report_date': run_report_date,
            'generated_by': self.env.user.name,
            'name': 'The Good Meat -' + company.name,
            'tin': '005-238-082-00008',
            'address': '104 Presidents Arcade 65 Presidents Avenue. B.F. Homes 1720 City Of Paranaque Ncr Fourth District Philippines',
            'headers': headers,
            'orders': order_report,
        }

        return returndata

    @api.model
    def _get_report_values(self, docids, data=None):
        if data:
            return self.action_print(data)
        else:
            raise UserError(_("Form content is missing, this report cannot be printed."))