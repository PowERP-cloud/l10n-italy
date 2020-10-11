#
# Copyright 2020 Didotech s.r.l. <https://www.didotech.com>
#
# Copyright 2020 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#

from odoo import models, fields, api
from odoo.exceptions import UserError


class DueDateManager(models.Model):
    _name = 'account.duedate_plus.manager'
    _description = 'Gestore scadenze fatture/note di credito'

    move_id = fields.Many2one(
        comodel_name='account.move',
        domain=[('journal_id.type', 'in', ['sale', 'sale_refund', 'purchase', 'purchase_refund'])],
        string='Registrazione contabile',
        requred=False
    )
    invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='Documento',
        requred=False
    )
    duedate_line_ids = fields.One2many(
        string='Righe scadenze',
        comodel_name='account.duedate_plus.line',
        inverse_name='duedate_manager_id',
        requred=False
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ORM METHODS OVERRIDE - begin

    @api.model
    def create(self, values):
        result = super().create(values)
        return result
    # end create

    @api.multi
    def write(self, values):
        result = super().write(values)
        return result
    # end write

    # ORM METHODS OVERRIDE - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # PUBLIC METHODS - begin

    @api.model
    def generate_duedates(self):

        # Remove obsolete duedates before computing the new ones
        if self.duedate_line_ids:
            self.duedate_line_ids.unlink()
        # end if

        if self.move_id:
            self._duedates_from_move()
        elif self.invoice_id:
            self._duedates_from_invoice()
        else:
            assert False,\
                '{} DueDate: at least one between mode_id ' \
                'and invoice_id must be assigned'.format(__name__)
        # end if

    # end generate_duedates

    # PUBLIC METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # CONSTRAINTS - begin
    # CONSTRAINTS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ONCHANGE - begin
    # ONCHANGE - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # VALIDATION METHODS - begin
    # VALIDATION METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # PRIVATE METHODS - begin

    @api.model
    def _duedates_from_move(self):
        # Compute payment terms and total
        # amount from the move
        payment_terms = self.move_id.payment_id
        move_type = self.move_id.move_type
        invoice_date = self.move_id.invoice_date
        total_amount = self.move_id.amount

        if not invoice_date:
            return False

        # If no payment terms generate only ONE due date line
        if not payment_terms:
            self.env['account.duedate_plus.line'].create({
                'duedate_manager_id': self.id,
                'due_date': invoice_date,
                'due_amount': total_amount,
                'payment_method_id': False,
            })

        else:
            due_dates = payment_terms.compute(total_amount, invoice_date)[0]
            new_dudate_lines = list()

            for due_date in due_dates:

                if move_type in ('receivable', 'payable_refund'):
                    payment_method = due_date[2]['inbound']
                elif move_type in ('payable', 'receivable_refund'):
                    payment_method = due_date[2]['outbound']
                else:
                    assert False, 'move_type for move must ' \
                                  'be receivable, payable, ' \
                                  'receivable_refund or payable_refund'
                # end if

                new_dudate_lines.append({
                    'duedate_manager_id': self.id,
                    'payment_method_id': payment_method.id,
                    'due_date': due_date[0],
                    'due_amount': due_date[1]
                })
            # end for

            self.env['account.duedate_plus.line'].create(new_dudate_lines)
        # end if
    # end _duedates_from_move

    @api.model
    def _duedates_from_invoice(self):

        # Compute payment terms and total
        # amount from the invoice
        payment_terms = self.invoice_id.payment_term_id
        invoice_date = self.invoice_id.date_invoice
        total_amount = self.invoice_id.amount_total

        # If no payment terms generate only ONE due date line
        if not payment_terms:
            self.env['account.duedate_plus.line'].create({
                'duedate_manager_id': self.id,
                'due_date': invoice_date,
                'due_amount': total_amount,
                'payment_method_id': False,
            })

        else:
            due_dates = payment_terms.compute(total_amount, invoice_date)[0]
            new_dudate_lines = list()

            for due_date in due_dates:

                invoice_type = self.invoice_id.account_id.user_type_id.type

                if invoice_type == 'receivable':
                    payment_method = due_date[2]['inbound']
                elif invoice_type == 'payable':
                    payment_method = due_date[2]['outbound']
                else:
                    assert False, 'account_id for invoice must' \
                                  'be receivable or payable'
                # end if

                new_dudate_lines.append({
                    'duedate_manager_id': self.id,
                    'payment_method_id': payment_method.id,
                    'due_date': due_date[0],
                    'due_amount': due_date[1]
                })
            # end for

            self.env['account.duedate_plus.line'].create(new_dudate_lines)
        # end if
    # end _duedates_from_invoice

    # PRIVATE METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# end DueDate
