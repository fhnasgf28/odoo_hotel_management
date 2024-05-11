from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError

class HotelRoom(models.Model):
    """Model That holds All details regarding hotel room"""
    _name = 'hotel.room'
    _description = 'rooms'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @tools.ormchache()
    def _get_default_uom_id(self):
        """Method for getting the default uom id"""
        return self.env.ref('uom.product_uom_unit')

    name = fields.Char(string='name', help='Name of the Room', index='trigram', required=True, translate=True)
    status = fields.Selection([('available', 'Available'),
                               ('reserved', 'Reserved'),
                               ('occupied', 'Occupied')], default='available', string='Status', help="Status of the Room", tracking=True)
    is_room_avail = fields.Boolean(string='Available', default=True, help='Check If the room is available')
    list_price = fields.Float(string='Rent', digits='Product Price', help='The rent of the Room')
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure', default=_get_default_uom_id, required=True,help="Default unit of measure used for all stock"
                                  " operations.")
