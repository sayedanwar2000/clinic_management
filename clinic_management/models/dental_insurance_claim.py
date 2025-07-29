from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DentalInsuranceClaim(models.Model):
    _name = 'dental.insurance.claim'
    _description = 'Dental Insurance Claim'

    name = fields.Char(string='Claim Reference', default=lambda self: _('New'))
    invoice_id = fields.Many2one('account.move', string='Related Invoice', required=True)
    patient_id = fields.Many2one(related='invoice_id.partner_id', string='Patient', store=True)
    insurance_company_id = fields.Many2one(
        'res.partner', string='Insurance Company',
        domain=[('is_insurance_company', '=', True)]
    )
    claim_date = fields.Date(default=fields.Date.today, required=True)
    amount_claimed = fields.Monetary(currency_field='currency_id', compute='_compute_amount_claimed', store=True)
    currency_id = fields.Many2one('res.currency', related='invoice_id.currency_id', store=True)
    insurance_coverage_percentage = fields.Float(default=0.0, digits=(16, 2))
    amount_reimbursed = fields.Monetary(currency_field='currency_id', compute='_compute_amount_reimbursed', store=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Claim Submitted'),
        ('waiting', 'Waiting For Approval'),
        ('reimbursed', 'Reimbursed'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ], default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name') == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('dental.insurance.claim') or _('New')
        return super().create(vals)

    @api.depends('invoice_id.amount_total')
    def _compute_amount_claimed(self):
        for rec in self:
            rec.amount_claimed = rec.invoice_id.amount_total
    
    @api.onchange('invoice_id')
    def _onchange_invoice_id(self):
        if self.invoice_id:
            patient = self.invoice_id.partner_id
            patient_rec = self.env['clinic.patient'].search([('partner_id', '=', patient.id)], limit=1)

            if not patient_rec:
                raise UserError(_("No patient record found linked to this customer."))

            if not patient_rec.insurance_company_id:
                raise UserError(_("This patient has no insurance company assigned."))

            self.insurance_company_id = patient_rec.insurance_company_id

    @api.depends('amount_claimed', 'insurance_coverage_percentage')
    def _compute_amount_reimbursed(self):
        for rec in self:
            rec.amount_reimbursed = rec.amount_claimed * (rec.insurance_coverage_percentage / 100.0)

    def action_submit_claim(self):
        self.ensure_one()
        self.state = 'waiting'

    def action_mark_reimbursed(self):
        self.ensure_one()

        if not self.amount_reimbursed:
            raise UserError(_("Amount reimbursed must be greater than 0."))

        if not self.invoice_id or self.invoice_id.payment_state == 'paid':
            raise UserError(_("The related invoice is either missing or already fully paid."))

        journal = self.env['account.journal'].search([('type', '=', 'cash')], limit=1)

        ctx = {
            'active_model': 'account.move',
            'active_ids': [self.invoice_id.id],
            'default_amount': self.amount_reimbursed,
            'default_journal_id': journal.id,
            'default_partner_id': self.insurance_company_id.id,
            'default_communication': f'Reimbursement for claim {self.name}',
        }

        wizard = self.env['account.payment.register'].with_context(ctx).create({})
        wizard.action_create_payments()
        self.state = 'reimbursed'

    def action_mark_rejected(self):
        self.ensure_one()
        self.state = 'rejected'

    def action_cancel_claim(self):
        self.ensure_one()
        self.state = 'cancelled'
