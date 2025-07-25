from odoo import models,fields, api

class DentalDiagnosis(models.Model):
    _name = 'dental.diagnosis'
    _description = 'Dental Diagnosis'
    _order = 'test_date desc'
    _rec_name = 'reference'

    case_id = fields.Many2one('dental.case', string="Dental Case", required=True, ondelete="cascade")
    diagnosis_test = fields.Char(string="Diagnosis Test", required=True)
    test_date = fields.Datetime(string="Test Date", default=fields.Datetime.now)
    test_result = fields.Text(string="Test Result")
    dentist_id = fields.Many2one('res.users', string="Dentist", default=lambda self: self.env.user)
    patient_id = fields.Char(related='case_id.patient_name', string="Patient", store=True)
    reference = fields.Char(string="Reference", readonly=True, copy=False, default='New')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('reference', 'New') == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code('dental.diagnosis') or 'New'
        return super().create(vals)

    def action_set_done(self):
        self.write({'state': 'done'})

    def action_set_cancelled(self):
        self.write({'state': 'cancelled'})
