from odoo import fields, models, tools, api, _


class RoomBookingLine(models.Model):
    """Model that handles the room booking form"""
    _name = "room.booking.line"
    _description = "Hotel Folio Line"

    # @tools.ormchache()
    # def _set_default_uom_id(self):
    #     return self.env.ref['uom.product_uom_day']

    booking_id = fields.Many2one("room.booking", string='Booking', help='Indicates The Room')
    checkin_date = fields.Datetime(string="Check In", help="you can choose the date,""otherwise sets to current Date",required=True)
    checkout_date = fields.Datetime(string="Check Out",help="You can choose the date,"
                                         " Otherwise sets to current Date",
                                    required=True)
    #     room id
    uom_qty = fields.Float(string="Duration", help="The Quantity converted into the UoM used by""the Product", readonly=True)
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure', help='This Will set the unit of measure used', readonly=True)

    # booking line visible
    booking_line_visible = fields.Boolean(default=False,string="Booking Line Visible",
                                              help="If True, then Booking Line "
                                                   "will be visible")
