from odoo import fields, models

class CleaningTeam(models.Model):
    ''' Model for creating cleaning team and assigns cleaning requests to each team'''
    _name = 'cleaning.team'
    _description = 'Cleaning Team'

    name = fields.Char(string='Team Name', help='Name Of the Team')
    team_head_id = fields.Many2one('res.users', string='Team Head', help="Choose the Team Head")
    member_ids = fields.Many2one('res.users', string='Member')