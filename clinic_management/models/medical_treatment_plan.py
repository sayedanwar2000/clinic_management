from odoo import models, fields, api

class MedicalTreatmentPlan(models.Model):
    _name = 'medical.treatment.plan'
    _description = 'Medical Treatment Plan'

    patient_id = fields.Many2one('clinic.patient', string='Patient', required=True)
    dentist_id = fields.Many2one('res.users', string='Responsible Dentist', required=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='Expected End Date')
    status = fields.Selection([
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='ongoing')
    diagnosis = fields.Text(string='Diagnosis')
    treatment_steps_ids = fields.One2many('treatment.step', 'plan_id', string='Treatment Steps')
    notes = fields.Text(string='Additional Notes')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
