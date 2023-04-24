# -*- coding: utf-8 -*-
{
	'name': 'FG Backend Custom',
	'version': '15.1.0.0',
	'category': 'FG/FG',
	'description': """
    	FG Backend Customization
        """,
	'depends': ['fg_custom'],
	'data': [
		'security/ir.model.access.csv',
		'data/ir_config_parameter_data.xml',
		'views/res_province_view.xml',
		'views/res_city_view.xml',
		'views/res_town_view.xml',
		'views/product_template_form_view.xml',
		'views/view_partner_property_form.xml',
		'views/view_order_form.xml',
		'views/menu_items.xml',
	],
	'demo': [],
	'license': 'LGPL-3',
	'qweb': [],
	'installable': True,
	'application': True,
	'auto_install': False,
	"assets": {
		"web.assets_backend": [
			"fg_backend_custom/static/src/js/form.js",
			"fg_backend_custom/static/src/js/ir_options.js",
		],
		"web.assets_qweb": ["fg_backend_custom/static/src/xml/base.xml"],
	},
}
