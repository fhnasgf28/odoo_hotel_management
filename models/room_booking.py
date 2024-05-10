# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class RoomBooking(models.Model):
    _name = "room.booking"
    _description = "Hotel Room Reservation"
    _inherit = ["mail.thread", 'mail.activity.mixin']

    name = fields.Char(string="Folio Number", readonly=True, index=True, default='New', help="Name Of Folio")
    company_id = fields.Many2one('res.company', string='Company', help='chose The Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner', string='Customer', help="Customers of Hotel", required=True, index=True,
                                 tracking=1, )  #domain (nanti diisiny)
    date_order = fields.Datetime(string="Order Date", required=True, copy=False,
                                 help="Creation date of draft/sent orders,"
                                      " Confirmation date of confirmed orders", default=fields.Datetime.now)
    is_checkin = fields.Boolean(default=False, string="Is Checkin", help="sets to True if the room is occupied")
    maintenance_request_sent = fields.Boolean(default=False, string="Maintenance Request" "or not",
                                              help="sets to True if the maintenance request send")
    checkin_date = fields.Datetime(string="Check In", help="Date Of CheckIn", default=fields.Datetime.now())
    checkout_date = fields.Datetime(string="Check Out",
                                    help="You can choose the date,"
                                         " Otherwise sets to current Date",
                                    required=True)
    hotel_policy = fields.Selection([
        ("prepaid", "On Booking"),
        ("manual", "On CheckIn"),
        ("picking", "On CheckOut"),
    ], default="manual", string="Hotel Policy", tracking=True)
    duration = fields.Integer(string="Duration in Days",
                              help="Number of days which will automatically "
                                   "count from the check-in and check-out "
                                   "date.", )
    invoice_button_visible = fields.Boolean(string="Invoice Button Display",
                                            help="Invoice button will be " "visible if this button is ""True")
    state = fields.Selection(selection=
    [
        ('draft', 'Draft'),
        ('reserved', 'Reserved'),
        ('checkin', 'CheckIn'),
        ('checkin', 'CheckIn'),
        ('checkout', 'CheckOut'),
        ('cancel', 'Cancel'),
        ('done', 'Done'),
    ], string='state', help="State of the Booking", default='draft', tracking=True)
    invoice_count = fields.Integer(compute='_compute_invoice_count', string='Invoice count',
                                   help="The Number of Invoice created")
    invoice_status = fields.Selection(selection=[('no_invoice', 'Nothing To Invoice'),
                                                 ('to_invoice', 'To Invoice'),
                                                 ('invoiced', 'Invoiced'),
                                                 ], string='Invoice Status', help="Status Of The Invoice",
                                      default='no_invoice', tracking=True)
    hotel_invoice_id = fields.Many2one("account.move", string="Invoice", help="Indicates The Invoice", copy=False)
    duration_visible = fields.Float(string="Duration", help="A Dummy field for Duration")
    need_service = fields.Boolean(default=False, string="Need Service",
                                  help="Check if a Service to be added with the booking")
    need_fleet = fields.Boolean(default=False, string="Need Vehicle",
                                help="Check if a fleet to be added with the Booking")
    need_food = fields.Boolean(default=False, string="Need Food", help="Check If A Event to be added with the booking")
    need_event = fields.Boolean(default=False, string="Need Event",
                                help="Check if a Event to be added with"
                                     " the Booking")
    # service_line_ids = fields.One2many("service.booking.line", "booking_id", string="Service",
    #                                    help="Hotel services details provided to" "Customer and it will included in" "the main Invoices.")
    # event_line_ids = fields.One2many('event.booking.line', 'booking_id', string="Event", help="Hotel Event "
    #                                                                                           "reservation detail.")
    # vehicle_line_ids = fields.One2many('fleet.booking.line', 'booking_id', string='Hotel room reservation detail.')
    room_line_ids = fields.One2many('room.booking.line', 'booking_id', string='Room', help="Hotel Room Reservation "
                                                                                           "detail.")
    # food_order_line_ids = fields.One2many('food.booking.line', 'booking_id', string='Food',
    #                                       help="Food details provided"
    #                                            " to Customer and"
    #                                            " it will included in the "
    #                                            "main invoice.", )
    user_id = fields.Many2one(comodel_name='res.partner', string="Invoice", compute='_compute_user_id',
                              help='sets the User Automatically', required=True, )  #ada domain
    pricelist_id = fields.Many2one(comodel_name='product.pricelist', string='Pricelist',
                                   compute='_compute_pricelist_id', store=True, readonly=False, required=True,
                                   tracking=1, help="If you change the pricelist,"
                                                    " only newly added lines"
                                                    " will be affected.")
    currency_id = fields.Many2one(string='Currency', help="This is the currency used",
                                  related='pricelist_id.currency_id', depends=['pricelist_id.currency_id'], )
    account_move = fields.Integer(string='Invoice Id', help='Id of the invoices created')
    amount_tax = fields.Monetary(string='Taxes', help='Total Tax Amount', store=True, compute='_compute_amount_untaxed',
                                 tracking=4)
    amount_untaxed = fields.Monetary(string='Total Untaxed Amount', help='This indicates the total untaxed''amount', store=True)
    amount_total = fields.Monetary(string="Total", store=True, help="The total Amount including Tax", compute='_compute_amount_untaxed', tracking=4)
    amount_untaxed_room = fields.Monetary(string="Room Untaxed", help='Untaxed Amount for Room', compute='_compute_amount_untaxed',tracking=5)
    amount_untaxed_food = fields.Monetary(string='Event Tax', help='Tax for event', compute='_compute_amount_untaxed', tracking=5)
    amount_taxed_event = fields.Monetary(string='Event Tax', help='Tax For Event', compute='_compute_amount_untaxed', tracking=5)
    amount_taxed_service = fields.Monetary(string='Service Tax', compute='_compute_amount_untaxed')
    amount_taxed_fleet = fields.Monetary(string='Fleet Tax', compute='_compute_amount_untaxed', help='This is the Total Amount for''Room', tracking=5)
    amount_total_event = fields.Monetary(string='Total Amount for Event', compute='_compute_amount_untaxed', help="This is the Total Amount for "
                                              "Event", tracking=5)
    amount_total_service = fields.Monetary(string='Total Amount for Service', compute='_compute_amount_untaxed', help='This is the Total Amount for''Fleet', tracking=5)
    amount_total_fleet = fields.Monetary(string='Total Amount for Fleet', compute='_compute_amount_untaxed', help="This is the Total Amount for "
                                              "Fleet", tracking=5)


    def action_view_invoices(self):
        return

    #     action reserve
    def action_reserve(self):
        return

    #     action check-in
    def action_checkin(self):
        return

    # action maintenance request
    def action_maintenance_request(self):
        return

    # amount total
    def _compute_amount_untaxed(self):
        return

