#
# Copyright 2017-20 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# Copyright 2020 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#


from odoo import models, api, fields
from odoo.tools.float_utils import float_is_zero


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

    no_delete_duedate_line_ids = fields.One2many(
        string='Righe scadenze',
        comodel_name='account.duedate_plus.line',
        related='duedate_manager_id.duedate_line_ids',
        readonly=False
    )

    check_duedates_payment = fields.Boolean(string='Ha pagamenti',
                                            compute='checks_payment')

    duedates_amount_current = fields.Monetary(
        string='Ammontare scadenze',
        compute='_compute_duedates_amounts'
    )

    duedates_amount_unassigned = fields.Monetary(
        string='Ammontare non assegnato a scadenze',
        compute='_compute_duedates_amounts'
    )

    def checks_payment(self):
        self.check_duedates_payment = False
        for line in self.duedate_line_ids:
            rec = self.env['account.payment.line'].search([
                ('move_line_id', '=', line.move_line_id.id)])
            if rec:
                self.check_duedates_payment = True

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ORM METHODS OVERRIDE - begin

    @api.model
    def create(self, values):
        # Apply modifications inside DB transaction
        new_invoice = super().create(values)

        # Return the result of the write command
        return new_invoice
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
    def update_duedates_and_move_lines(self):
        # Update account.duedate_plus.line records
        self._update_duedates()

        # Update account.move.line records according to account.duedate_plus.line records
        #self._update_credit_debit_move_lines()
    # end update_duedates_and_move_lines


    @api.multi
    def action_update_duedates_and_move_lines(self):
        # Update account.duedate_plus.line records
        for invoice in self:
            invoice.update_duedates_and_move_lines()
        # end for
    # end update_duedates_and_move_lines


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
            updates['payment_term_id'] = pt and pt.id or False

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

        # may be empty if account_total is zero
        if len(head_lines) == 0:
            return move_lines

        # Altre linee che vanno MANTENNUTE
        new_lines = [
            ml
            for ml in move_lines
            if (ml[2]['tax_ids'] or ml[2]['tax_line_id'])
        ]

        # Dati relativi al conto
        prototype_line = head_lines[0][2]

        for duedate in self.duedate_manager_id.duedate_line_ids:

            # Create the new line
            new_line_dict = prototype_line.copy()

            # Update - maturity date
            new_line_dict['date_maturity'] = duedate.due_date

            # Update - reference to the duedate line
            new_line_dict['duedate_line_id'] = duedate.id

            # Update - set amount
            if new_line_dict['credit']:
                new_line_dict['credit'] = duedate.due_amount
            elif new_line_dict['debit']:
                new_line_dict['debit'] = duedate.due_amount
            else:
                pass
            # end if

            # Update - payment method
            new_line_dict['payment_method'] = duedate.payment_method_id.id

            new_lines.append(
                (0, 0, new_line_dict)
            )
        # end for

        return new_lines
    # end finalize_invoice_move_lines

    # PUBLIC METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ONCHANGE METHODS - begin

    @api.onchange('duedate_line_ids')
    def _onchange_duedate_line_ids(self):
        self._compute_duedates_amounts()
    # end _onchange_duedate_line_ids

    @api.onchange('payment_term_id', 'date_invoice')
    def _onchange_payment_term_id_date_invoice(self):
        self.update_duedates_and_move_lines()
    # end _onchange_payment_term_id_date_invoice

    @api.onchange('amount_total')
    def _onchange_amount_total(self):

        if self.duedates_amount_current == 0:
            ratio = 0
        else:
            ratio = self.duedates_amount_unassigned / self.duedates_amount_current
        # end if

        for line in self.duedate_line_ids:
            line.proposed_new_value = line.due_amount * (1 + ratio)
        # end for
    # end _onchange_amount_total

    @api.onchange('duedates_amount_unassigned')
    def _onchange_duedates_amount_unassigned(self):
        '''
        Reset proposed_new_value if duedates_amount_unassigned is zero
        '''
        precision = self.env.user.company_id.currency_id.rounding

        if float_is_zero(
                self.duedates_amount_unassigned, precision_rounding=precision):
            for line in self.duedate_line_ids:
                line.proposed_new_value = 0
            # end for
        # end if
    # end _onchange_duedates_amount_unassigned

    # ONCHANGE METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # PROTECTED METHODS - begin

    @api.multi
    def _update_duedates(self):

        # Do nothing if invoice date is not set
        if not self.date_invoice:
            return
        # end if

        # Ensure duedate_manager is configured
        self._get_duedate_manager()

        # Generate duedates
        duedate_line_list = self.duedate_manager_id.generate_duedate_lines()

        # Generate the commands list for the ORM update method
        updates_list = list()

        # Remove old records
        if self.duedate_line_ids:
            updates_list += [(2, duedate_line.id, 0) for duedate_line in self.duedate_line_ids]
        # end if

        # Create new records
        if duedate_line_list:
            updates_list += [(0, 0, duedate_line) for duedate_line in duedate_line_list]
        # end if

        # Update the record
        if updates_list:
            self.update({'duedate_line_ids': updates_list})
        # end if
    # end _update_duedates

    @api.model
    def _update_credit_debit_move_lines(self):

        # Should not be necessary ...just in case
        if not self.line_ids:
            return
        # end if

        # Extract credit and debit lines
        lines_cd = list()
        lines_other = list()

        for line in self.line_ids:
            line._compute_line_type()
            line_type = line.line_type
            if line_type in ('credit', 'debit'):
                lines_cd.append(line)
            else:
                lines_other.append(line)
            # end if
        # end for

        # Build the move line template dictionary
        move_line_template = lines_cd[0].copy_data()[0]
        del move_line_template['move_id']  # 'move_id' removed because it will be automatically set by the update method

        # List of modifications to move lines one2many field
        move_lines_mods = list()

        # Add the new move lines
        for duedate_line in self.duedate_line_ids:
            new_data = move_line_template.copy()

            # Set the linked account.duedate_plus.line record
            new_data['duedate_line_id'] = duedate_line.id

            # Set the date_maturity field
            new_data['date_maturity'] = duedate_line.due_date

            # Set the amount
            if new_data['credit'] > 0:
                new_data['credit'] = duedate_line.due_amount
            else:
                new_data['debit'] = duedate_line.due_amount
            # end if

            move_lines_mods.append(
                (0, False, new_data)
            )
        # end for

        # Schedule deletion of old lines
        move_lines_mods += [(4, line.id) for line in lines_other]

        # Schedule deletion of old lines
        move_lines_mods += [(2, line.id) for line in lines_cd]

        # Save changes
        self.update({'line_ids': move_lines_mods})

    # end _update_credit_debit_move_lines

    @api.model
    def _get_duedate_manager(self):
        '''
        Return the duedates manager for this invoice
        :return: The duedates manager object for the invoice
                 (account.duedate_plus.manager)
        '''

        # Check if duedate manager is missing
        duedate_mgr_miss = not self.duedate_manager_id

        # Add the Duedate Manager if it's missing
        if duedate_mgr_miss:
            self._create_duedate_manager()
        # end if

        # Return the manager
        return self.duedate_manager_id
    # end get_duedate_manager

    @ api.model
    def _create_duedate_manager(self):
        # Add the Duedates Manager
        duedate_manager = self.env['account.duedate_plus.manager'].create({
            'invoice_id': self.id
        })

        self.update({'duedate_manager_id': duedate_manager})
    # end _create_duedate_manager

    @api.multi
    @api.depends('duedate_line_ids', 'amount_total')
    def _compute_duedates_amounts(self):

        for inv in self:
            # Somma ammontare di ciascuna scadenza
            lines_total = sum(
                # Estrazione ammontare da ciascuna scadenza
                map(lambda l: l.due_amount, self.duedate_line_ids)
            )

            # Aggiornamento campo ammontare scadenze
            self.duedates_amount_current = lines_total

            # Aggiornamento campo ammontare non assegnato a scadenze
            self.duedates_amount_unassigned = self.amount_total - lines_total
        # end for
    # end _compute_duedate_lines_amount

    # PROTECTED METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# end AccountInvoice
