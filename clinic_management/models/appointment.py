from odoo import models, fields, api


class DentalAppointment(models.Model):
    _name = 'dental.appointment'
    _description = 'Dental Appointment'
    _rec_name = 'reference'

    # General Info
    patient_id = fields.Many2one('clinic.patient', string='Patient')
    patient_type = fields.Selection([
        ('new', 'New Patient'),
        ('existing', 'Existing Patient')
    ], string="Patient Type", default='new')
    age = fields.Integer(string="Age", required=True)
    phone = fields.Char(related='patient_id.phone', string="Phone", store=True, readonly=False)
    email = fields.Char(related='patient_id.email', string="Email", store=True, readonly=False)

    # Appointment Info
    appointment_date = fields.Datetime(string="Appointment Date", required=True)
    dentist_id = fields.Many2one('res.users', string="Dentist", required=True)

    # Address Info
    street = fields.Char(related='patient_id.street', string="Street", store=True, readonly=False)
    street2 = fields.Char(related='patient_id.street2', string="Street2", store=True, readonly=False)
    city = fields.Char(related='patient_id.city', string="City", store=True, readonly=False)
    state_id = fields.Many2one("res.country.state", related="patient_id.state_id", string="State", store=True,
                               readonly=False)
    zip = fields.Char(related='patient_id.zip', string="ZIP", store=True, readonly=False)
    country_id = fields.Many2one('res.country', related='patient_id.country_id', string="Country", store=True,
                                 readonly=False)

    # Other Info
    description = fields.Text(string="Description")
    other_info = fields.Text(string="Other Info")
    case_ids = fields.One2many('dental.case', 'appointment_id', string="Dental Cases")

    # Meta
    reference = fields.Char(string="Reference", readonly=True, copy=False, default='New')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('done', 'Done'),
    ], string="Status", default='draft')

    @api.model
    def create(self, vals):
        print(vals.get('reference'))
        if vals.get('reference', 'New') == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code('dental.appointment') or 'New'
            print(vals.get('reference'))
            print(self.env['ir.sequence'].next_by_code('dental.appointment'))
        print(vals.get('reference'))
        return super().create(vals)

    def action_confirm(self):
        for rec in self:
            rec.write({
                'state': 'confirmed'
            })

    def action_cancel(self):
        for rec in self:
            rec.write({
                'state': 'cancelled'
            })

    def action_create_dental_case(self):
        for appointment in self:
            self.env['dental.case'].create({
                'appointment_id': appointment.id,
                'patient_type': appointment.patient_type,
                'patient_name': appointment.patient_id.name,
                'age': appointment.age,
                'street': appointment.street,
                'street2': appointment.street2,
                'city': appointment.city,
                'state_id': appointment.state_id.id,
                'zip': appointment.zip,
                'country_id': appointment.country_id.id,
                'phone': appointment.phone,
                'email': appointment.email,
                'appointment_time': appointment.appointment_date,
                'dentist_id': appointment.dentist_id.id,
            })
            appointment.write({
                'state': 'done'
            })


