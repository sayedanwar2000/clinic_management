from odoo import models, fields

class DentalTreatment(models.Model):
    _name = 'dental.treatment'
    _description = 'Dental Treatment'

    patient_id = fields.Many2one('res.partner')
    tooth = fields.Char()
    treatment = fields.Char()
    charge = fields.Float()
    remarks = fields.Char()
    dentist_id = fields.Many2one('res.users')
    date = fields.Date()
