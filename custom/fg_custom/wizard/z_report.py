# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import pytz
from datetime import datetime, date, timedelta
from pytz import timezone, UTC
from dateutil.relativedelta import relativedelta

class ZReport(models.TransientModel):
    _name = "z.report"
    _description = "Z Report"

    #start_at = fields.Date(string='Start Date', required=True)
    end_at = fields.Date(string='End Date', required=True, default=fields.Date.context_today)
    #user_id = fields.Many2one('res.users', string='Cashier User')
    #session_ids = fields.Many2many('pos.session', domain="[('state', '=', 'closed')]", string='Sessions', required=True)


    # @api.onchange('start_at', 'end_at', 'user_id')
    # def onchange_end_at(self):
    #     if self.start_at and self.end_at:
    #         # 00: 00:00
    #         # date_start = fields.Datetime.to_string(self.start_at)
    #         # 23: 59:59
    #         date_stop = fields.Datetime.to_string(self.end_at + relativedelta(hours=23, minutes=59, seconds=59))
    #         #if self.user_id:
    #             #return {'domain': {'session_ids': [('start_at', '>=', date_start), ('start_at', '<=', date_stop), ('state', '=', 'closed'), ('user_id', '=', self.user_id.id)]}}
    #         session_ids = {'domain': {'session_ids': [('start_at', '<=', date_stop), ('state', '=', 'closed')]}}
    #         return session_ids

    def action_print_all(self):
        # for selected date only
        date_start = fields.Datetime.to_string(self.end_at)
        date_stop = fields.Datetime.to_string(self.end_at + relativedelta(hours=23, minutes=59, seconds=59))
        session_ids = self.env['pos.session'].search([('start_at', '>=', date_start), ('start_at', '<=', date_stop),('state', '=', 'closed')])

        #for accumulated
        accumulated_session_ids = self.env['pos.session'].search([('start_at', '<=',date_stop),('state', '=', 'closed')])
        data = {'session_id': session_ids.ids, 'accumulated_session_id': accumulated_session_ids.ids} #selected day and accumulated sessions
        return self.env.ref('fg_custom.z_pos_report').report_action(None, data=data)
