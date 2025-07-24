from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_type_clinic = fields.Selection([
        ('medicine', 'Medicine'),
        ('device', 'Device'),
        ('tool', 'Tool'),
        ('consumable', 'Consumable'),
    ], string='Product Type')

    unit_of_measure = fields.Char(string='Unit of Measure')
    min_quantity = fields.Float(string='Minimum Quantity')
    supplier_id = fields.Many2one('res.partner', string='Supplier', domain="[('supplier_rank', '>', 0)]")
    last_purchase_date = fields.Date(
        string='Last Purchase Date',
        compute='_compute_last_purchase_date',
        store=False,
        readonly=True
    )

    @api.depends('name')
    def _compute_last_purchase_date(self):
        for product in self:
            last_date = False
            lines = self.env['purchase.order.line'].search([
                ('product_id', '=', product.id),
                ('order_id.state', 'in', ['purchase', 'done']),
            ], order='date_approve desc', limit=1)

            if lines:
                last_date = lines.order_id.date_order
            product.last_purchase_date = last_date

    def trigger_low_stock_action(self):
        product_ids = self.search([])
        for product in product_ids:
            if product.min_quantity and product.qty_available < product.min_quantity:
                # 1. Post a warning message
                message = f"Available quantity of {product.display_name} is below the minimum threshold!"
                product.message_post(body=message)

                # 2. Create a Purchase Order
                if product.supplier_id:
                    purchase_order = self.env['purchase.order'].create({
                        'partner_id': product.supplier_id.id,
                        'order_line': [(0, 0, {
                            'product_id': product.id,
                            'name': product.name,
                            'product_qty': product.min_quantity * 2,
                            'product_uom': product.uom_id.id,
                            'price_unit': product.standard_price,
                            'date_planned': fields.Date.today(),
                        })]
                    })
                    product.message_post(
                        body=f"Auto purchase order created: #{purchase_order.name}")
