from odoo import models, fields

class DentalPrescription(models.Model):
    _name = 'dental.prescription'
    _description = 'Dental Prescription '

    case_id = fields.Many2one('dental.case', string="Dental Case", required=True, ondelete="cascade")
    dentist_id = fields.Many2one('res.users', string="Dentist", default=lambda self: self.env.user)
    date = fields.Date(default=fields.Date.today, string="Date")
    patient_id = fields.Char(related='case_id.patient_name', string="Patient", store=True)
    medicine = fields.Char(string="Medicine")
    medicine_type = fields.Selection([('tablet', 'Tablet'), ('capsule', 'Capsule')], string="Medicine Type")
    dose = fields.Float(string="Dose")
    frequency = fields.Char(string="Frequency")
    duration = fields.Integer(string="Duration")
    notes = fields.Char(string="Notes")