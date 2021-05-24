# Copyright (c) 2020
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        """
        override the action adding duedates and due date
        """
        ids = super().action_invoice_create(grouped, final)
        for invoice in self.env['account.invoice'].browse(ids):
            # requirement: date_invoice or date_effective
            if invoice.date_invoice or invoice.date_effective:
                date_invoice = invoice.date_invoice and invoice.date_invoice \
                               or invoice.date_effective
                # and payment_term_id
                if invoice.payment_term_id:
                    manager = invoice._get_duedate_manager()
                    # generate dudates
                    manager.write_duedate_lines()
                    # update due date according to payment term
                    pterm = invoice.payment_term_id
                    pterm_list = pterm.with_context(
                        currency_id=invoice.company_id.currency_id.id).compute(
                        value=1, date_ref=date_invoice)[0]
                    invoice.date_due = max(line[0] for line in pterm_list)
                # end if
            # end if
        # end for
        return ids
