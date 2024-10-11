from odoo import api, fields, models, tools

class ServiceBookingLine(models.Model):
    """Model that handles the service booking form"""
    _name = "service.booking.line"
    _description = "Hotel Service Line"

    @tools.ormcache()
    def _get_default_uom_id(self):
        """Returns default product uom unit"""
        return self.env.ref('uom.product_uom_unit')

    booking_id = fields.Many2one("room.booking", string="Booking", help="Indicates the room booking", ondelete="cascade")
    service_id = fields.Many2one("hotel.service", string="Service", help="Indicates the service")
    description = fields.Char(string="Description", related='service_id.name', help="Description of the service")
    uom_qty = fields.Float(string='Qty', default=1.0,)
    uom_id = fields.Many2one('uom.uom', readonly=True, string='Unit of Measure', default=_get_default_uom_id)