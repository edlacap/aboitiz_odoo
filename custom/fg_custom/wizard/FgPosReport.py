# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import pytz
from datetime import datetime, date, timedelta
from pytz import timezone, UTC
from dateutil.relativedelta import relativedelta

class FgPosReportForm(models.TransientModel):
    _name = "fg.pos.report"
    _description = "POS Report"

    start_at = fields.Date(string='Start Date', required=True, default=fields.Date.context_today)
    end_at = fields.Date(string='End Date', required=True, default=fields.Date.context_today)
    report_type = fields.Selection([
        ('sales_report', 'Sales Report'),
        ('refund_report', 'Refund Report'),
        ('pwd_sc_discount', 'PWD/SC Discount Report')],
        string='Report Type', required=True, default='direct',
        help="Select report type")


    def action_print_all(self):
        date_start = fields.Datetime.to_string(self.start_at)
        date_stop = fields.Datetime.to_string(self.end_at + relativedelta(hours=23, minutes=59, seconds=59))  # end upto 23:59:59
        data = {'report_type': self.report_type, 'date_start': date_start, 'date_stop': date_stop}
        return self.env.ref('fg_custom.fg_pos_report').report_action(None, data=data)
