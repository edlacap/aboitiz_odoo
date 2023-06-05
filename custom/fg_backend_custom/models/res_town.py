from odoo import models, fields


class ResTown(models.Model):
    _name = 'res.town'
    _description = 'Town'

    name = fields.Char('Town')
