from odoo import models, fields, api


class DentalCase(models.Model):
    _name = 'dental.case'
    _description = 'Dental Case'

    name = fields.Char(string="Appointment", readonly=True, required=True, copy=False, default='New')
    patient_type = fields.Selection([
        ('new', 'New Patient'),
        ('returning', 'Returning Patient'),
    ], string="Patient Type", default='new', required=True)

    patient_name = fields.Char(string="Patient Name", required=True)
    age = fields.Integer(string="Age")

    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state", string="State")
    zip = fields.Char(string="ZIP")
    country_id = fields.Many2one('res.country', string="Country")

    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")

    appointment_time = fields.Datetime(string="Appointment Time", required=True)
    dentist_id = fields.Many2one('res.users', string="Dentist", required=True)
    appointment_id = fields.Many2one('dental.appointment', string="Appointment")
    diagnosis_ids = fields.One2many('dental.diagnosis', 'case_id', string="Diagnosis")
    prescription_ids = fields.One2many('dental.prescription', 'case_id', string="Prescriptions")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('diagnosis', 'Diagnosis'),
        ('treatment', 'Treatment'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft', tracking=True)

    description = fields.Html(string="Description")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('dental.case') or 'New'
        return super().create(vals)

    def action_set_diagnosis(self):
        self.write({'state': 'diagnosis'})

    def action_set_treatment(self):
        self.write({'state': 'treatment'})

    def action_set_done(self):
        self.write({'state': 'done'})

    def action_set_cancelled(self):
        self.write({'state': 'cancelled'})

    def action_open_add_diagnosis_wizard(self):
        return {
            'name': 'Add Diagnosis',
            'type': 'ir.actions.act_window',
            'res_model': 'dental.diagnosis.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_case_id': self.id,
                'default_patient_id': self.patient_name,
                'default_dentist_id': self.dentist_id.id,
            }
        }

    def action_open_prescription_wizard(self):
        self.ensure_one()
        return {
            'name': 'Create Prescription',
            'type': 'ir.actions.act_window',
            'res_model': 'prescription.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.patient_name,
                'default_dentist_id': self.dentist_id.id,
                'default_dental_case': self.name,
            }
        }





