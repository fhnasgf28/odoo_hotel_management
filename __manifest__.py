# -*- coding: utf-8 -*-
{
    'name': "hotel_management",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'account', 'event', 'fleet', 'lunch'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/room_booking_views.xml',
        'views/hotel_menu_view.xml',
        'views/hotel_room_views.xml',
        'views/hotel_floor_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True
}

