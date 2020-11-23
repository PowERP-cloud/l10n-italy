#
# Copyright (c) 2020
#
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        ids = super().action_invoice_create(grouped, final)
        for invoice in self.env['account.invoice'].browse(ids):
            if invoice.date_invoice or invoice.date_effective:
                if invoice.payment_term_id:
                    manager = invoice._get_duedate_manager()
                    manager.write_duedate_lines()

