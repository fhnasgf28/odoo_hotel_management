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
    maintenance_request_sent = fields.Boolean(default=False, string="Maintenance Request" "or not", help="sets to True if the maintenance request send")
    checkin_date = fields.Datetime(string="Check In", help="Date Of CheckIn", default=fields.Datetime.now())
    hotel_policy = fields.Selection([
        ("prepaid", "On Booking"),
        ("manual", "On CheckIn"),
        ("picking", "On CheckOut"),
    ], default="manual", string="Hotel Policy", tracking=True)
    duration = fields.Integer(string="Duration in Days",
                              help="Number of days which will automatically "
                                   "count from the check-in and check-out "
                                   "date.", )
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