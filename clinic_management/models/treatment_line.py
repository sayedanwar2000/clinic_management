from odoo import models, fields, api


class ClinicServiceLine(models.Model):
    _name = 'treatment.line'
    _description = 'Treatment Line'

    patient_id = fields.Many2one('clinic.patient', string="Patient")
    product_id = fields.Many2one('product.product', string="Treatment", domain=[('sale_ok', '=', True)], required=True)
    quantity = fields.Float(string="Quantity", default=1.0)
    price_unit = fields.Float(string="Unit Price")
    subtotal = fields.Float(string="Subtotal", compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            if line.product_id:
                line.price_unit = line.product_id.lst_price
