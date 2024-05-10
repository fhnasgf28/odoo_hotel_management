from odoo import fields, models, tools, api, _


class RoomBookingLine(models.Model):
    """Model that handles the room booking form"""
    _name = "room.booking.line"
    _description = "Hotel Folio Line"
    _rec_name = 'room_id'

    booking_id = fields.Many2one("room.booking", string='Booking', help='Indicates The Room')
