from odoo import models, fields, api


class DentalAppointment(models.Model):
    _name = 'dental.appointment'
    _description = 'Dental Appointment'

    # General Info
    patient_id = fields.Many2one('res.partner', string='Patient')
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
        if vals.get('reference', 'New') == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code('dental.appointment') or 'New'
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
