#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import api, fields, models
from .mixin_base import BaseMixin


class AccountInvoice(models.Model, BaseMixin):
    _inherit = "account.invoice"

    def write(self, vals):
        if 'company_bank_id' in vals:
            if self.state == 'open':
                self.move_id.write({
                        'company_bank_id': vals['company_bank_id'],
                        # 'bank_2_print_selector': 'company',
                })
            # end if
        # end if
        if 'counterparty_bank_id' in vals:
            if self.state == 'open':
                self.move_id.write({
                        'counterparty_bank_id': vals['counterparty_bank_id'],
                        # 'bank_2_print_selector': 'partner',
                })
            # end if
        # end if
        return super().write(vals)
    # end write

