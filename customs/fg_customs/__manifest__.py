# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
   'name': 'FG Custom Addons',
    'version': '1.0',
    'category': 'FG/FG',
    'description': """
    Pilmico custom addons
        """,
    'depends': ['product','website', 'account', 'point_of_sale'],
    'data': [
     'views/fg_customer_master.xml',
     'views/fg_custom_product.xml',
     'static/src/xml/models_extend.xml'
    ],
    'author': "1FG",
     'demo': [],
    'qweb': ['static/src/xml/Screens/ReceiptScreen/OrderReceipt.xml',
                 'static/src/xml/Screens/ClientListScreen/ClientDetailsEdit.xml',
                'static/src/xml/models_extend.xml'],
    'installable': True,
    'application': True,
    'auto_install': False
}
