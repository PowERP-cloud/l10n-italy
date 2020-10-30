#
# Copyright 2020 Didotech s.r.l. <https://www.didotech.com>
#
# Copyright 2020 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#


from odoo import models, fields, api
from odoo.tools.float_utils import float_is_zero


class AccountMove(models.Model):
    _inherit = 'account.move'

    duedate_manager_id = fields.One2many(
        string='Gestore scadenze',
        comodel_name='account.duedate_plus.manager',
        inverse_name='move_id',
    )

    duedate_line_ids = fields.One2many(
        string='Righe scadenze',
        comodel_name='account.duedate_plus.line',
        related='duedate_manager_id.duedate_line_ids',
        readonly=False
    )

    duedate_lines_amount = fields.Float(
        related='duedate_manager_id.duedate_lines_amount'
    )

    duedates_amount_current = fields.Monetary(
        string='Ammontare scadenze',
        compute='_compute_duedates_amounts'
    )

    duedates_amount_unassigned = fields.Monetary(
        string='Ammontare non assegnato a scadenze',
        compute='_compute_duedates_amounts'
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ORM METHODS OVERRIDE - begin

    @api.model
    def create(self, values):
        # Apply modifications inside DB transaction
        new_move = super().create(values)

        # Return the result of the write command
        return new_move
    # end create

    @api.multi
    def write(self, values):
        result = super().write(values)

        for move in self:

            duedate_mgr_miss = not move.duedate_manager_id
            payment_terms_updated = 'payment_term_id' in values

            # Compute the due dates if payment terms was changed or duedates
            # manager was missing
            # if duedate_mgr_miss:
            #     move.generate_duedates()
            # end if
        # end for

        return result
    # end write

    # ORM METHODS OVERRIDE - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ONCHANGE METHODS - begin

    @api.onchange('duedate_line_ids')
    def _onchange_duedate_line_ids(self):
        self._compute_duedates_amounts()
    # end _onchange_duedate_line_ids

    @api.onchange('amount')
    def _onchange_amount(self):
        if self.duedates_amount_current == 0:
            ratio = 0
        else:
            ratio = self.duedates_amount_unassigned / self.duedates_amount_current
        # end if

        for line in self.duedate_line_ids:
            line.proposed_new_value = line.due_amount * (1 + ratio)
        # end for
    # end _onchange_amount

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

    # NB: il campo 'peyment_term_id' è definito nel modulo 'account_move_plus'
    #     che è una dipendenza di questo modulo
    @api.onchange('payment_term_id')
    def _onchange_payment_term_id(self):
        # Update account.duedate_plus.line records
        self._update_duedates()

        # Update account.move.line records according to account.duedate_plus.line records
        self._update_credit_debit_move_lines()
    # end _onchange_duedate_line_ids

    # ONCHANGE METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # PUBLIC METHODS - begin

    @api.model
    def _update_duedates(self):
        # Ensure duedate_manager is configured
        self._get_duedate_manager()

        # Generate duedates
        duedate_line_list = self.duedate_manager_id.generate_duedate_lines()

        # Generate the commands list for the ORM update method
        # Remove old records
        updates_list = list(
            [(2, duedate_line.id, 0) for duedate_line in self.duedate_line_ids]
            +
            # Create new records
            [(0, 0, duedate_line) for duedate_line in duedate_line_list]
        )

        # Update the record
        self.update({'duedate_line_ids': updates_list})
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
            if line.line_type in ('credit', 'debit'):
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

    # PUBLIC METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # COMPUTE METHODS - begin

    @api.multi
    @api.depends('duedate_line_ids')
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
            self.duedates_amount_unassigned = self.amount - lines_total
        # end for
    # end _compute_duedate_lines_amount

    # COMPUTE METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # PROTECTED METHODS - begin

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

    def _create_duedate_manager(self):
        # Add the Duedates Manager
        duedate_manager = self.env['account.duedate_plus.manager'].create({
            'move_id': self.id
        })

        self.update({'duedate_manager_id': duedate_manager})
    # end _create_duedate_manager

    # PROTECTED METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# end AccountMove
