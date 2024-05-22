from odoo import fields, models

class AccountMoveLine(models.Model):
    '''adding product type field to account move line model'''

    _inherit = 'account.move.line'

    product_type = fields.Selection([('room', 'Room'),('food', 'Food'),
                                     ('event', 'Event'),
                                     ('service', 'Service'),
                                     ('fleet', 'Fleet')],
                                    string='Product Type', help='Choose the product type')