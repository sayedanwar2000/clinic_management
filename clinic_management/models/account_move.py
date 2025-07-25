from odoo import fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    dental_case_id = fields.Many2one(
        'dental.case', 
        string='Dental Case', 
        ondelete='set null', 
        help="Related Dental Case"
    )

    def open_invoice_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }
