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

    @api.model
    def _validate_duedates(self):

        # ID not set, delay validation to when the
        # object creation is completed
        if not self.id:
            return
        # end if

        # Perform validations reading from the database (the values are on the
        # DB inside our transaction).
        # If error raise exception ...the transaction will be rolled back and
        # no modification will be performed on DB.

        # Check for correctness of the dates
        error_date = self._validate_duedates_date()
        if error_date:
            return error_date
        # end if

        # Check for correctness of the total amount of the duedates
        error_amount = self._validate_duedates_amount()
        if error_amount:
            return error_amount
        # end if

    # end _validate

    @api.model
    def _validate_duedates_date(self):
        """
        Enforces the following constraint:

        the first due_date can be prior to the mode date, every other due_date
        must be later than or equal to the move date.
        """

        if self.invoice_id:
            invoice_date = self.invoice_id.date_invoice
        elif self.move_id:
            invoice_date = self.move_id.invoice_date
        else:
            assert False
        # end if

        # Sorted list of dates (least date -> least index)
        duedates_list = sorted([duedate.due_date for duedate in self.duedate_line_ids])

        if len(duedates_list) <= 1:
            # No duedates or just one date -> validation successful
            return None

        elif duedates_list[1] >= invoice_date:
            # The second due_date is not prior than the invoice date ->
            # -> validation successful.
            # Since the duedates_list is a sorted list, every other date with
            # index > 1 will be >= duedates_list[1] and consequently a
            # valid date
            return None

        else:  # Validation FAILED
            # When the execution arrives here the following conditions are TRUE:
            # - there duedates
            # - the first and second due_dates are prior to the invoice date
            # so the dates are not valid!!
            return {
                'title': 'Scadenza - Data di scadenza',
                'message': 'Solo la prima scadenza può essere precedente alla data fattura'
            }

        # end if

    # end _validate_duedates_date

    @api.model
    def _validate_duedates_amount(self):
        """
        Enforces the following constraint:

        the sum of the amount of each the duedate related to this account.move
        must be equal to the account.move amount
        """

        if self.invoice_id:
            precision = self.invoice_id.currency_id.decimal_places
            amount_total = self.amount_total
        elif self.move_id:
            precision = self.move_id.currency_id.decimal_places
            amount_total = self.amount
        else:
            assert False
        # end if

        # Get the list of the other due_dates, ordered by due_date ascending
        duedates_amounts = [
            round(duedate.due_amount, precision)
            for duedate in self.duedate_ids
        ]

        # If there are duedates check the amounts
        amounts_sum = sum(duedates_amounts)
        difference = round(amounts_sum - amount_total, precision)

        # There must be at least one due date to proceed with validation,
        # if no due date has been defined yet skip the validation
        if duedates_amounts and (difference != 0):  # Validation FAILED
            return {
                'title': 'Scadenze - Totale import',
                'message': 'Il totale degli importi delle scadenze deve coincidere'
                'con il totale della registrazione ({})'.format(amount_total)
            }

        else:  # Validation succesful!
            return None
        # end if
    # end _validate_duedates_amount

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
                    payment_method = due_date[2]['credit']
                elif move_type in ('payable', 'receivable_refund'):
                    payment_method = due_date[2]['debit']
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
                    payment_method = due_date[2]['credit']
                elif invoice_type == 'payable':
                    payment_method = due_date[2]['debit']
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
