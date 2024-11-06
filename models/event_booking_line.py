
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
    currency_id = fields.Many2one(string='Currency', related='booking_id.pricelist_id.currency_id', help="Total Price Currency", store=True, precompute=True)
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_price_subtotal', help='Total Price Excluding Tax', store=True)
    price_tax = fields.Float(string="Total Tax", compute="_compute_price_subtotal", help="Tax amount", store=True)
    price_total = fields.Float(string="Total", compute="_compute_price_subtotal", store=True)
    state = fields.Selection(related='booking_id.state', string='Order Status', copy=False)

    @api.depends('price_unit', 'uom_qty', 'tax_ids')
    def _compute_price_subtotal(self):
        for line in self:
            tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
            totals = list(tax_results['totals'].values())[0]
            amount_untaxed = totals['amount_untaxed']
            amount_tax = totals['amount_tax']
            line.update({
                'price_subtotal': amount_untaxed,
                'price_tax': amount_tax,
                'price_total': amount_untaxed + amount_tax,
            })
            if self.env.context.get('import_file', False) and not self.env.user. \
                    user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_recordset(['invoice_repartition_line_ids'])

    def _convert_to_tax_base_line_dict(self):
        self.ensure_one()
        return self.env['account.tax']._convert_to_tax_base_line_dict(
            self,
            partner=self.booking_id.partner_id,
            currency=self.currency_id,
            taxes=self.tax_ids,
            price_unit=self.price_unit,
            quantity=self.uom_qty,
            price_subtotal=self.price_subtotal,
        )
