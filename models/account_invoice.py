#
# Copyright (c) 2020
#
from odoo import models, api, fields, _
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_move_create(self):
        super().action_move_create()
        # move_model = self.env['account.move']
        for inv in self:
            if inv.move_id.type is False:
                inv.move_id.write({'type': self.type})

            if inv.move_id.line_ids:
                for line in inv.move_id.line_ids:
                    if line.account_id:
                        account_type = self.env['account.account.type'].search(
                            [('id', '=', line.account_id.user_type_id.id)])
                        if account_type:
                            if account_type.type == 'payable':
                                line.write({'due_dc': 'D'})
                            elif account_type.type == 'receivable':
                                line.write({'due_dc': 'C'})

                    if inv.payment_term_id:
                        pass
                    print(line.due_dc)
        return True


