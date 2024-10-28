
from odoo import api, fields, models


class EventBookingLine(models.Model):
    _name = 'event.booking.line'
    _description = "Hotel Event Line"
    _rec_name = 'event_id'

    booking_id = fields.Manyone('room.booking', string='Booking', ondelete='cascade')
    event_id = fields.Manyone('event.event', string='Event', help='Choose the event')
    ticket_id = fields.Manyone('product.product', string='Ticket', domain=[('detailed_type', '=', 'event')])
    description = fields.Char(string='Description', help='Detailed description of the event', related='event_id.display_name')
    uom_qty = fields.Float(string='Quantity', default=1,)
    uom_id = fields.Manyone('uom.uom', readonly=True, string='Unit of Measure', related='ticket_id.uom_id', help='This will set the unit of measure used')
    price_unit = fields.Float(related='ticket_id.lst_price', string='Price', digits='Product Price')
    tax_ids = fields.Many2many('account.tax', 'hotel_event_order_line_taxes_rel', 'event_id', 'tax_id', related='ticket_id.taxes_id',string='Taxes',
                               domain=[('type_tax_use', '=', 'sale')])