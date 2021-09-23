# -*- coding: utf-8 -*-
from odoo import models, fields, tools, SUPERUSER_ID, _, api


class ProductInherit(models.Model):
    _inherit = "product.template"
    _description = "inherit product.template"

    fg_product_id = fields.Char("Product ID")
    fg_product_status = fields.Selection([('Y', 'Active'), ('N', 'Inactive')], string='Status', required=False)
    fg_product_class = fields.Many2one(
        'fg.product.class',
        string="Product Class",
        change_default=True,
        help="Select Product Class for the current product")


class FgProductClass(models.Model):
    _name = "fg.product.class"
    _description = "Product Class"

    name = fields.Char('Name', required=True)
    desc = fields.Char('Description', required=False)


class FgSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"
    _description = "inherit product.supplierinfo"

    fg_avg_cost = fields.Float("Average Cost", help="Average Cost")
