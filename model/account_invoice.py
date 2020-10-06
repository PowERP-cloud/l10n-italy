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

            payment_by_date = {
                terms['due_date']: (terms['inbound'], terms['outbound'])
                for terms in map(lambda tline:
                                 tline.compute_due_date(inv.date_invoice),
                                 inv.payment_term_id.line_ids)
            }

            if inv.move_id.line_ids:
                for line in inv.move_id.line_ids:
                    if line.account_id:
                        account_type = self.env['account.account.type'].search(
                            [('id', '=', line.account_id.user_type_id.id)])
                        if account_type:
                            method = payment_by_date.get(line.date_maturity,
                                                         (False, False))

                            if account_type.type == 'payable':
                                line.due_dc = 'D'
                                line.payment_method = method[1]
                            elif account_type.type == 'receivable':
                                line.due_dc = 'C'
                                line.payment_method = method[0]
                # end for
            # end if
        # end for

        return True
    # end action_move_create

# end AccountInvoice
