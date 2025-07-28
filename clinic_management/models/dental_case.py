from odoo import models, fields, api, _
from odoo.exceptions import UserError


class DentalCase(models.Model):
    _name = 'dental.case'
    _description = 'Dental Case'

    name = fields.Char(string="Appointment", readonly=True, required=True, copy=False, default='New')
    patient_type = fields.Selection([
        ('new', 'New Patient'),
        ('returning', 'Returning Patient'),
    ], string="Patient Type", default='new', required=True)

    patient_id = fields.Many2one('clinic.patient', string="Patient", required=True)
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
    diagnosis_ids = fields.One2many('dental.diagnosis', 'case_id', string="Diagnosis", store=True)

    treatment_line_ids = fields.One2many('treatment.line', 'case_id', string='Treatment Lines')
    invoice_ids = fields.One2many('account.move', 'dental_case_id', string='Invoices')
    invoice_count = fields.Integer(string='Invoices Count', compute='_compute_invoice_count')
    treatment_plan_ids = fields.One2many('medical.treatment.plan', 'patient_id', string='Treatment Plans',compute='_compute_treatment_plan')

    

    def _compute_treatment_plan(self):
        for line in self:
            line.treatment_plan_ids = self.env['medical.treatment.plan'].search([('patient_id','=',line.patient_id.id)])
            
    def _compute_invoice_count(self):
        for case in self:
            case.invoice_count = len(case.invoice_ids)

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

    from datetime import date

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id:
            self.age = self.patient_id.age
            self.phone = self.patient_id.phone
            self.email = self.patient_id.email
            self.street = self.patient_id.street
            self.street2 = self.patient_id.street2
            self.city = self.patient_id.city
            self.state_id = self.patient_id.state_id.id
            self.zip = self.patient_id.zip
            self.country_id = self.patient_id.country_id.id

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
                'default_patient_id': self.patient_id.id,
                'default_dentist_id': self.dentist_id.id,
            }
        }

    def action_create_invoice(self):
        self.ensure_one()

        if not self.treatment_line_ids:
            raise UserError(_("You must add at least one treatment before creating an invoice."))

        if not self.patient_id:
            raise UserError(_("No patient linked to this case."))

        invoice_lines = []
        for line in self.treatment_line_ids:
            if not line.product_id:
                raise UserError(_("Treatment line does not have an associated product."))

            account = line.product_id.property_account_income_id or line.product_id.categ_id.property_account_income_categ_id
            if not account:
                raise UserError(_("Please define an income account for the product %s.") % line.product_id.name)

            invoice_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
                'name': line.product_id.name,
                'account_id': account.id,
            }))

        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.patient_id.partner_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': invoice_lines,
            'ref': self.name,
            'dental_case_id': self.id,

        }

        invoice = self.env['account.move'].create(invoice_vals)

        return {
            'name': _('Invoice'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',
        }

    def action_open_invoice_wizard(self):
        self.ensure_one()
        action = self.env.ref('clinic_management.action_dental_invoice_wizard').sudo().read()[0]
        action['context'] = {'default_case_id': self.id}
        return action