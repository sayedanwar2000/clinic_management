from odoo import models, fields, api

class ClinicPatient(models.Model):
    _name = 'clinic.patient'
    _description = 'Clinic Patient'

    name = fields.Char(string='Patient Name', required=True)
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
    insurance_company_id = fields.Many2one('res.partner', string='Insurance Company')
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
