from odoo import models, fields, api


class DiagnosisWizard(models.TransientModel):
    _name = 'dental.diagnosis.wizard'
    _description = 'Add Diagnosis Wizard'

    case_id = fields.Many2one('dental.case', string="Dental Case", required=True)
    diagnosis_test = fields.Char(string="Diagnosis Test", required=True)
    test_date = fields.Datetime(string="Test Date", default=fields.Datetime.now)
    test_result = fields.Text(string="Test Result")
    dentist_id = fields.Many2one('res.users', string="Dentist", default=lambda self: self.env.user)
    patient_id = fields.Char(related='case_id.patient_name', string="Patient", store=True)

    def action_add_diagnosis(self):
        self.env['dental.diagnosis'].create({
            'case_id': self.case_id.id,
            'diagnosis_test': self.diagnosis_test,
            'test_date': self.test_date,
            'test_result': self.test_result,
            'dentist_id': self.dentist_id.id,
        })
        return {'type': 'ir.actions.act_window_close'}
