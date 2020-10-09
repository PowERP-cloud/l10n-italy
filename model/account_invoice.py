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
                if invoice.duedate_manager_id:
                    invoice.duedate_manager_id.generate_duedates()
                # end if
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

        self.ensure_one()

        move_lines = super().finalize_invoice_move_lines(move_lines)

        # Linee di testata che rappresentano le scadenze da RIMPIAZZARE
        head_lines = [
            ml
            for ml in move_lines
            if (ml[2]['tax_ids'] is False and ml[2]['tax_line_id'] is False)
        ]

        # Altre linee che vanno MANTENNUTE
        new_lines = [
            ml
            for ml in move_lines
            if (ml[2]['tax_ids'] or ml[2]['tax_line_id'])
        ]

        # Dati relativi al conto
        prototype_line = head_lines[0][2]
        account = self.env['account.account'].browse(prototype_line['account_id'])
        account_type = account.user_type_id.type

        for duedate in self.duedate_manager_id.duedate_line_ids:

            new_line_dict = prototype_line.copy()

            new_line_dict['maturity_date'] = duedate.due_date

            if new_line_dict['credit']:
                new_line_dict['credit'] = duedate.due_amount
            elif new_line_dict['debit']:
                new_line_dict['debit'] = duedate.due_amount
            else:
                assert False
            # end if

            new_line_dict['payment_method'] = duedate.payment_method_id

            if account_type == 'payable':
                new_line_dict['due_dc'] = 'D'
            elif account_type == 'receivable':
                new_line_dict['due_dc'] = 'C'
            # end if

            new_lines.append(
                (0, 0, new_line_dict)
            )
        # end for

        return new_lines
    # end finalize_invoice_move_lines
# end AccountInvoice
