#
# Copyright (c) 2020
#
from odoo import models, api
from odoo.exceptions import UserError


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    @api.model
    def get_payment_method_config(self, payment_method_code):
        raise UserError('Non implementato nella classe base')
