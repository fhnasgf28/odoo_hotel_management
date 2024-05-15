# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class FoodBooking(models.Model):
    _name = "food.booking"
    _description = "Hotel Food Line"
    _rec_name = 'food_id'

    @tools.ormcache()
    def _get_default_uom_id(self):
        '''method for getting the default uom id'''
        return self.env.ref('uom.product_uom_unit')

    booking_id = fields.Many2one('room.booking', string='Booking', help='Shows the room Booking', ondelete='cascade')
    food_id = fields.Many2one('lunch.product', string='Product', help='Indicates the food Product')
    description = fields.Char(string='Description', help='Description of Food Product', related='food_id.display_name')
    uom_qty = fields.Float(string='qty', default=1, help='The quantity converted into the UoM used by the product')
    uom_id = fields.Many2one('uom.uom', readonly=True,
                             string="Unit of Measure",
                             default=_get_default_uom_id, help="This will set "
                                                               "the unit of"
                                                               " measure used")
