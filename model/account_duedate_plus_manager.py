# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
#
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import datetime
from odoo import models, fields, api


MOVE_TYPE_INV_CN = ('out_invoice', 'out_refund', 'in_invoice', 'in_refund')


class DueDateManager(models.Model):
    _name = 'account.duedate_plus.manager'
    _description = 'Gestore scadenze fatture/note di credito'

    move_id = fields.Many2one(
        comodel_name='account.move',
        domain=[('journal_id.type', 'in', ['sale', 'sale_refund', 'purchase',
                                           'purchase_refund'])],
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
    def write_duedate_lines(self):
        '''
        Generate and WRITE the account.duedate_plus.line records
        associated with this manager
        '''
        # Remove obsolete duedates before computing the new ones
        if self.duedate_line_ids:
            self.duedate_line_ids.unlink()
        # end if

        # Get the new lines
        new_dudate_lines = self.generate_duedate_lines()

        # Create the new lines (if any)
        if new_dudate_lines:
            self.env['account.duedate_plus.line'].create(new_dudate_lines)
        # end if
    # end write_duedate_lines

    @api.model
    def generate_duedate_lines(self):
        '''
        Returns a list of dict, one for each account.duedate_plus.line record
        to be generated
        '''

        if self.move_id:
            new_dudate_lines = self._duedates_from_move()
        elif self.invoice_id:
            new_dudate_lines = self._duedates_from_invoice()
        else:
            return []
        # end if

        return new_dudate_lines
    # end generate_duedate_lines

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
    # PUBLIC API - begin

    @api.model
    def update_amount(self):
        self._compute_duedate_lines_amount()
    # end update_amount

    # PUBLIC API - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # VALIDATION METHODS - begin

    @api.model
    def validate_duedates(self):

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
            invoice_date = self.move_id.date_invoice

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
            amount_total = self.invoice_id.amount_total
        elif self.move_id:
            precision = self.move_id.currency_id.decimal_places
            amount_total = self.move_id.amount
        else:
            assert False
        # end if

        # Get the list of the other due_dates, ordered by due_date ascending
        duedates_amounts = [
            round(duedate.due_amount, precision)
            for duedate in self.duedate_line_ids
        ]

        # If there are duedates check the amounts
        amounts_sum = sum(duedates_amounts)
        difference = round(amounts_sum - amount_total, precision)

        # There must be at least one due date to proceed with validation,
        # if no due date has been defined yet skip the validation
        if duedates_amounts and (difference != 0):  # Validation FAILED
            return {
                'title': 'Scadenze - Totale importi',
                'message': 'Il totale degli importi delle scadenze ({}) deve coincidere'
                ' con il totale della registrazione ({}). Differenza: ({})'.format(
                    amounts_sum, amount_total, difference
                )
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

        # Check if the move is an invoice or a credit note
        is_invoice_or_credit_note = self.move_id.type in MOVE_TYPE_INV_CN

        # Do something only if there are move lines to use for calculations
        # and the move is an invoice or a credit note
        if not is_invoice_or_credit_note:
            return list()

        elif not self.move_id.line_ids:
            return list()

        else:

            # Compute payment terms and total amount from the move
            payment_terms = self.move_id.payment_term_id
            doc_type = self.move_id.type

            if self.move_id.date_effective:
                invoice_date = self.move_id.date_effective
            else:
                invoice_date = self.move_id.invoice_date
            # end if

            total_amount = self.move_id.amount
            type_error_msg = 'move_type for move must be one of: receivable, ' \
                             'payable_refund, payable, receivable_refund'
            partner_id = self.move_id.partner_id

            return self._duedates_common(
                payment_terms, doc_type, invoice_date, total_amount,
                type_error_msg, partner_id
            )

        # end if

    # end _duedates_from_move

    @api.model
    def _duedates_from_invoice(self):
        # Compute payment terms and total amount from the invoice
        payment_terms = self.invoice_id.payment_term_id
        doc_type = self.invoice_id.type
        if self.invoice_id.date_effective:
            invoice_date = self.invoice_id.date_effective
        elif self.invoice_id.date_invoice:
            invoice_date = self.invoice_id.date_invoice
        else:
            invoice_date = fields.Date.today()

        total_amount = self.invoice_id.amount_total
        type_error_msg = 'account for invoice must be one of: receivable, ' \
                         'payable_refund, payable, receivable_refund'
        partner_id = self.invoice_id.partner_id

        return self._duedates_common(
            payment_terms, doc_type, invoice_date, total_amount, type_error_msg,
            partner_id
        )
    # end _duedates_from_invoice

    @api.model
    def _duedates_common(
        self,
        payment_terms, doc_type, invoice_date, total_amount, type_error_msg,
            partner_id
    ):
        '''
        Duedates generation function: this is the part of the algorithm in
        common between move and invoice
        :param payment_terms: payment terms record
        :param doc_type: type of "document"
        (receivable, payable, receivable_refund, payable_refund)
        :param invoice_date: date of the invoice
        :param total_amount: total amount of the invoice
        :param type_error_msg: msg to be displayed if the doc_type is invalid
        :return: a list of dictionary, each dict represents a duedate record
        '''
        new_dudate_lines = list()

        if not invoice_date:
            return new_dudate_lines
        # end if

        # If no payment terms generate only ONE due date line
        # with due_date equal to the invoice date
        if not payment_terms:

            # Generate a default duedate line only if the
            # invoice amount is not zero
            if total_amount > 0:
                idate = invoice_date.strftime('%Y-%m-%d')
                inv_date = self._get_split_date_period(partner_id, doc_type,
                                                       idate)
                new_dudate_lines.append({
                    'duedate_manager_id': self.id,
                    'due_date': inv_date,
                    'due_amount': total_amount,
                    'payment_method_id': False,
                })
            else:
                return new_dudate_lines
            # end if

        else:
            add_tax = False
            if payment_terms.first_duedate_tax and self.invoice_id:
                amount_to_compute = self.invoice_id.amount_untaxed
                tax = self.invoice_id.amount_tax
                add_tax = True
            else:
                tax = 0.0
                amount_to_compute = total_amount
            # end if

            due_dates = payment_terms.compute(amount_to_compute, invoice_date)[0]
            for due_date in due_dates:
                if doc_type in ('out_invoice', 'in_refund'):
                    payment_method = due_date[2]['credit']
                elif doc_type in ('in_invoice', 'out_refund'):
                    payment_method = due_date[2]['debit']
                else:
                    assert False, type_error_msg
                # end if
                if add_tax:
                    due_amount = due_date[1] + tax
                    add_tax = False
                else:
                    due_amount = due_date[1]
                # end if

                line_date = self._get_split_date_period(partner_id, doc_type,
                                                        due_date[0])

                new_dudate_lines.append({
                    'duedate_manager_id': self.id,
                    'payment_method_id': payment_method.id,
                    'due_date': line_date,
                    'due_amount': due_amount
                })
            # end for
        # end if

        return new_dudate_lines
    # end _duedates_common

    @api.model
    def _get_split_date_period(self, parent_id, doc_type, date):
        comparison_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        if parent_id.partner_duedates_dr_ids:
            for period in parent_id.partner_duedates_dr_ids:
                enable_period = False
                if doc_type in ('out_invoice', 'in_refund'):
                    enable_period = period.enable_customer
                elif doc_type in ('in_invoice', 'out_refund'):
                    enable_period = period.enable_supplier

                if enable_period and (
                        period.period_id.date_start <= comparison_date <=
                        period.period_id.date_end
                ):
                    return period.split_date.strftime('%Y-%m-%d')
        return date

    # PRIVATE METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# end DueDate
