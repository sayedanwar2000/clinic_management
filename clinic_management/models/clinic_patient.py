from odoo import models, fields, api

class ClinicPatient(models.Model):
    _name = 'clinic.patient'
    _description = 'Clinic Patient'

    name = fields.Char(string='Patient Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Related Contact', ondelete='cascade')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender')
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    image_1920 = fields.Binary(string='Image')
    blood_type = fields.Selection([
        ('a+', 'A+'), ('a-', 'A-'),
        ('b+', 'B+'), ('b-', 'B-'),
        ('ab+', 'AB+'), ('ab-', 'AB-'),
        ('o+', 'O+'), ('o-', 'O-'),
    ], string='Blood Type')
    allergies = fields.Text(string='Allergies')
    medical_history = fields.Text(string='Medical History')
    current_conditions = fields.Text(string='Current Conditions')
    #prescription_ids = fields.One2many('clinic.prescription', 'patient_id', string='Prescriptions')
    treatment_plan_ids = fields.One2many('medical.treatment.plan', 'patient_id', string='Treatment Plans')
    #appointment_ids = fields.One2many('clinic.appointment', 'patient_id', string='Appointments')
    insurance_company_id = fields.Many2one(
        'res.partner', string='Insurance Company', required=True,
        domain=[('is_insurance_company', '=', True)]
    )
    insurance_number = fields.Char(string='Insurance Number')
    active = fields.Boolean(string='Active', default=True)
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state", string="State")
    zip = fields.Char(string="ZIP")
    country_id = fields.Many2one('res.country', string="Country")

    treatment_line_ids = fields.One2many(
        comodel_name='treatment.line',
        inverse_name='patient_id',
        string="Treatment Lines",
    )


    appointment_ids = fields.One2many(
        'dental.appointment',
        'patient_id',
        string="Appointments"
    )

    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                today = fields.Date.today()
                age = today.year - patient.birth_date.year - (
                    (today.month, today.day) < (patient.birth_date.month, patient.birth_date.day)
                )
                patient.age = age
            else:
                patient.age = 0


    @api.model
    def create(self, vals):
        partner_vals = {
            'name': vals.get('name'),
            'phone': vals.get('phone'),
            'email': vals.get('email'),
            'street': vals.get('street'),
            'street2': vals.get('street2'),
            'city': vals.get('city'),
            'state_id': vals.get('state_id'),
            'zip': vals.get('zip'),
            'country_id': vals.get('country_id'),
            'is_company': False,
            'customer_rank': 1,
        }
        partner = self.env['res.partner'].create(partner_vals)
        vals['partner_id'] = partner.id
        return super().create(vals)

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if record.partner_id:
                record.partner_id.write({
                    'name': record.name,
                    'phone': record.phone,
                    'email': record.email,
                    'street': record.street,
                    'street2': record.street2,
                    'city': record.city,
                    'state_id': record.state_id.id,
                    'zip': record.zip,
                    'country_id': record.country_id.id,
                })
        return res
