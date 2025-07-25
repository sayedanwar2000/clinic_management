from odoo import models, fields, api

class PrescriptionWizard(models.TransientModel):
    _name = 'prescription.wizard'
    _description = 'Create Prescription Wizard'

    patient_id = fields.Char(string="Patient", required=True)
    dentist_id = fields.Many2one('res.users', string="Dentist", required=True)
    date = fields.Date(default=fields.Date.today, string="Date")
    dental_case = fields.Char(string="Dental Case", required=True)

    line_ids = fields.One2many('prescription.wizard.line', 'wizard_id', string="Medicines")

    def action_create_prescription(self):
        self.env['clinic.prescription'].create({
            'patient': self.patient_id,
            'dentist_id': self.dentist_id.id,
            'date': self.date,
            'dental_case': self.dental_case,
            'line_ids': [(0, 0, {
                'medicine': line.medicine,
                'medicine_type': line.medicine_type,
                'dose': line.dose,
                'frequency': line.frequency,
                'duration': line.duration,
                'notes': line.notes,
            }) for line in self.line_ids]
        })
        return {'type': 'ir.actions.act_window_close'}
