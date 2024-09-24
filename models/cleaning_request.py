from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CleaningRequest(models.Model):
    _name = "cleaning.request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "sequence"
    _description = "Cleaning request"

    sequence = fields.Char(string="Sequence", readonly=True, default='New', copy=False, tracking=True, help="Sequence for identifying the request")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('assign', 'Assigned'),
        ('ongoing', 'Cleaning'),
        ('support', 'Waiting For Support'),
        ('done', 'Completed')],
        string="State",
        default='draft', help="State of cleaning request")
    cleaning_type = fields.Selection(selection=[('room', 'Room'),
                                                ('hotel', 'Hotel'),
                                                ('vehicle', 'Vehicle')],
                                     required=True, tracking=True,
                                     string="Cleaning Type",
                                     help="Choose what is to be cleaned")
    room_id = fields.Many2one('hotel.room', string="Room", help="Choose the room")
    hotel = fields.Char(string='Hotel', help="Cleaning request space in hotel")
    vehicle_id = fields.Many2one('fleet.vehicle.model', string='Vehicle', help='Cleaning request from vehicle')
    support_team_ids = fields.Many2many('res.users', string="Support Team", help="Support team members")
    support_reason = fields.Char(string='Support', help="Support Reason")
    description = fields.Char(string="Description",
                              help="Description about the cleaning")
    team_id = fields.Many2one('cleaning.team', string="Team",
                              required=True,
                              tracking=True,
                              help="Choose the team")
    head_id = fields.Many2one('res.users', string='Head', related='team_id.team_head_id', help="Head of cleaning team")
    assigned_id = fields.Many2one('res.users', string="Assigned To")
    domain_partner_ids = fields.Many2many('res.partner', string='Domain Partner')
