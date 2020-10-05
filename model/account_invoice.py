# -*- coding: utf-8 -*-
#
# Copyright 2017-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#


from odoo import models, api, fields, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    duedate_ids = fields.One2many(
        string='Scadenze',
        comodel_name='account.move.line',
        related='move_id.duedate_ids',
        readonly=False,
    )

    @api.multi
    def action_move_create(self):
        super().action_move_create()
        # move_model = self.env['account.move']
        for inv in self:
            if inv.move_id.type is False:
                inv.move_id.write({'type': self.type})
            # end if

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
                # end for
                        # if inv.payment_term_id:
                        #     if account_type:
                        #         if account_type.type == 'payable' and \
                        #                 inv.payment_term_id.payment_method_outbound:
                        #             pass
                        #         elif account_type.type == 'receivable' and inv.payment_term_id.payment_method_inbound:
                        #             pass
                    # print(line.due_dc)
            # end if
        # end for

        return True
    # end action_move_create

# end AccountInvoice
