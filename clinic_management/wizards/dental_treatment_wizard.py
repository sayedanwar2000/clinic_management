from odoo import models, fields

class TreatmentWizard(models.TransientModel):
    _name = 'treatment.wizard'
    _description = 'Create Treatment Wizard'

    patient_id = fields.Many2one('res.partner', string="Patient", required=True)
    date = fields.Date(string="Date", default=fields.Date.today)
    tooth = fields.Char(string="Tooth")
    dentist_id = fields.Many2one('res.users', string="Dentist", default=lambda self: self.env.user)
    treatment_line_ids = fields.One2many('treatment.wizard.line', 'wizard_id', string="Treatments")
    treatment_charge = fields.Float(string="Treatment Charge", compute="_compute_treatment_charge", store=True)
    description = fields.Text(string="Description")

    @api.depends('treatment_line_ids.charge')
    def _compute_treatment_charge(self):
        for rec in self:
            rec.treatment_charge = sum(line.charge for line in rec.treatment_line_ids)

    def action_create_treatments(self):
        for line in self.treatment_line_ids:
            self.env['dental.treatment'].create({
                'patient_id': self.patient_id.id,
                'tooth': self.tooth,
                'date': self.date,
                'treatment': line.name,
                'charge': line.charge,
                'remarks': line.remarks,
                'dentist_id': self.dentist_id.id,
            })
