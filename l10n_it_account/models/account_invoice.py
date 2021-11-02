# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    amount_net_pay = fields.Float(string='Net to pay',
                                  store=True,
                                  digits=dp.get_precision('Account'),
                                  compute='_compute_net_pay')

    @api.depends('amount_total')
    def _compute_net_pay(self):
        for inv in self:
            inv.amount_net_pay = inv.amount_total
    # and _compute_net_pay