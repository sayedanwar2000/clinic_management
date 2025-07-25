from odoo import models, fields, api

class TreatmentStep(models.Model):
    _name = 'treatment.step'
    _description = 'Treatment Step'

    plan_id = fields.Many2one('medical.treatment.plan', string='Treatment Plan', required=True)
    name = fields.Char(string='Step Name', required=True)
    date = fields.Date(string='Execution Date')
    progress = fields.Selection([
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], string='Progress', default='not_started')
    notes = fields.Text(string='Notes')
