#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import api, fields, models
from .mixin_base import BaseMixin


class AccountInvoice(models.Model, BaseMixin):
    _inherit = "account.invoice"

    @api.model
    def create(self, vals):
        new_invoice: AccountInvoice = super().create(vals)
        company_bank = new_invoice.company_bank_id
        counter_bank = new_invoice.counterparty_bank_id

        if new_invoice.type in ('out_invoice', 'out_refund') and company_bank:
            new_invoice.partner_bank_id = company_bank
        elif new_invoice.type in ('in_invoice', 'in_refund') and counter_bank:
            new_invoice.partner_bank_id = counter_bank
        # end if

        return new_invoice
    # end create

    def write(self, vals):
        if 'company_bank_id' in vals:

            lines = self.move_id.line_ids.filtered(
                lambda
                    x: x.reconciled is False and x.payment_order.id is False
            )

            lines.write({
                'company_bank_id': vals['company_bank_id']
            })

            if self.state == 'open':
                self.move_id.write({
                        'company_bank_id': vals['company_bank_id'],
                })
            # end if
            if self.state == 'draft':
                self.write({
                    'partner_bank_id': vals['company_bank_id'],
                })
            # end if

        # end if
        if 'counterparty_bank_id' in vals:

            lines = self.move_id.line_ids.filtered(
                lambda
                    x: x.reconciled is False and x.payment_order.id is False
            )

            lines.write({
                'counterparty_bank_id': vals[
                    'counterparty_bank_id']
            })

            if self.state == 'open':
                self.move_id.write({
                        'counterparty_bank_id': vals['counterparty_bank_id'],
                })
            # end if
            if self.state == 'draft':
                self.write({
                    'partner_bank_id': vals['counterparty_bank_id'],
                })
            # end if
        # end if
        return super().write(vals)
    # end write

