# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class FgAuditReport(models.Model):
    _name = 'report.fg_custom.report_fg_audit_report'
    _inherit = 'audit.log'
    _description = 'Audit Log Report'

    def action_print(self, data):
        headers = 'Date,Resource Name,User,Last Updated On, Field, Old Value, New Value'
        run_report_date = datetime.today().strftime('%Y-%m-%d')
        company = self.env.company
        report_type = 'Audit Log Report'
        audit_report = []

        auditRec = self.env['audit.log'].search([('create_date', '>=', data.get('date_start'))])

        for logs in auditRec:
            updated_details = []
            content = logs._get_content()

            for det in content:
                updated_details.append({'field': det[0],
                                        'oldValue': det[1],
                                        'newValue': det[2]
                                        })
            # print(updated_details)

            audit_report.append({'date': fields.Datetime.to_string(logs.create_date),
                                 'name': logs.name,
                                 'user': logs.user_id.name,
                                 'last_update_on': fields.Datetime.to_string(logs.write_date),
                                 'data': updated_details
                                 })
        returndata = {
            'report_type': report_type,
            'run_report_date': run_report_date,
            'generated_by': self.env.user.name,
            'name': 'The Good Meat -' + company.name,
            'tin': '005-238-082-00008',
            'address': '104 Presidents Arcade 65 Presidents Avenue. B.F. Homes 1720 City Of Paranaque Ncr Fourth District Philippines',
            'headers': headers,
            'auditLogs': audit_report,
            'date_from': data.get('date_start').split(' ')[0],
            'date_to': data.get('date_stop').split(' ')[0]
        }

        return returndata

    @api.model
    def _get_report_values(self, docids, data=None):
        if data:
            return self.action_print(data)
        else:
            raise UserError(_("Form content is missing, this report cannot be printed."))