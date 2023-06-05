from odoo import models, fields


class ResProvince(models.Model):
    _name = 'res.province'
    _description = 'Province'

    name = fields.Char('Province')
