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

    duedate_manager_id = fields.One2many(
        string='Gestore scadenze',
        comodel_name='account.duedate_plus.manager',
        inverse_name='invoice_id',
    )

    duedate_line_ids = fields.One2many(
        string='Righe scadenze',
        comodel_name='account.duedate_plus.line',
        related='duedate_manager_id.duedate_line_ids',
        readonly=False
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ORM METHODS OVERRIDE - begin

    @api.model
    def create(self, values):
        # Apply modifications inside DB transaction
        new_invoice = super().create(values)

        # Add the Duedates Manager
        new_invoice.duedate_manager_id = new_invoice.env[
            'account.duedate_plus.manager'
        ].create({
            'invoice_id': new_invoice.id
        })

        # Compute the due dates
        new_invoice.duedate_manager_id.generate_duedates()

        # Return the result of the write command
        return new_invoice
    # end create

    @api.multi
    def write(self, values):
        result = super().write(values)

        # If payment terms was changed recompute the due dates
        if 'payment_term_id' in values:
            for invoice in self:
                invoice.duedate_manager_id.generate_duedates()
            # end for
        # end if
        return result
    # end write

    # ORM METHODS OVERRIDE - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # PROTECTED METHODS

    # PROTECTED METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @api.multi
    def action_move_create(self):
        super().action_move_create()
        # move_model = self.env['account.move']
        for inv in self:

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Copia dati da testata fattura

            updates = dict()

            if inv.move_id.type is False:
                updates['type'] = self.type
            # end if

            # Data fattura
            updates['invoice_date'] = inv.date_invoice

            # Termini di pagamento
            pt = inv.payment_term_id
            updates['payment_id'] = pt and pt.id or False

            # Update the "move"
            inv.move_id.write(updates)
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            # Update the DueManager adding the reference to the "account.move"
            inv.duedate_manager_id.write({'move_id': inv.move_id.id})

        # end for

        return True
    # end action_move_create

    @api.multi
    def finalize_invoice_move_lines(self, move_lines):
        move_lines = super().finalize_invoice_move_lines(move_lines)
        # return move_lines
        for inv in self:

            payment_by_date = {
                terms[0]: (terms[2]['inbound'], terms[2]['outbound'])
                for terms in inv.payment_term_id.compute(
                    value=inv.amount_total, date_ref=inv.date_invoice
                )[0]
            }
            for tline in move_lines:
                line = tline[2]
                if line['account_id']:
                    account = self.env['account.account'].browse(
                        line['account_id'])
                    account_type = self.env['account.account.type'].search(
                        [('id', '=', account.user_type_id.id)])
                    if account_type:
                        method = payment_by_date.get(
                            str(line['date_maturity']),
                            (False, False)
                        )

                        if account_type.type == 'payable':
                            line['due_dc'] = 'D'
                            line['payment_method'] = method[1].id
                        elif account_type.type == 'receivable':
                            line['due_dc'] = 'C'
                            line['payment_method'] = method[0].id
                # end for
            # end if
        # end for
        return move_lines
    # end finalize_invoice_move_lines
# end AccountInvoice
