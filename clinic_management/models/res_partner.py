from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_insurance_company = fields.Boolean(string='Is an Insurance Company', default=False, help="Check if this contact is an insurance company.")