from odoo import models, fields, api

class DentalInvoiceWizard(models.TransientModel):
    _name = 'dental.invoice.wizard'
    _description = 'Wizard to Show Dental Case Invoices'

    case_id = fields.Many2one('dental.case', string='Dental Case', readonly=True)
    invoice_ids = fields.One2many('account.move', compute='_compute_invoice_ids', string='Invoices')

    @api.depends('case_id')
    def _compute_invoice_ids(self):
        for wizard in self:
            wizard.invoice_ids = self.env['account.move'].search([
                ('dental_case_id', '=', wizard.case_id.id),
                ('move_type', '=', 'out_invoice')
            ])
