#
# Copyright 2020 Didotech s.r.l. <https://www.didotech.com>
#
# Copyright 2020 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#


from odoo import models, fields, api


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
    # PROTECTED METHODS

    def _create_duedate_manager(self, move):
        # Add the Duedates Manager
        move.duedate_manager_id = move.env[
            'account.duedate_plus.manager'
        ].create({
            'move_id': move.id
        })

    # end _create_duedate_manager

    # PROTECTED METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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
            duedate_generate = duedate_mgr_miss or 'payment_term_id' in values

            # Add the Duedates Manager if it's missing
            if duedate_mgr_miss:
                self._create_duedate_manager(move)
            # end if

            # Compute the due dates if payment terms was changed or duedates
            # manager was missing
            if duedate_generate:
                move.duedate_manager_id.generate_duedates()
            # end if
        # end for

        return result
    # end write

    # ORM METHODS OVERRIDE - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @api.onchange('duedate_line_ids')
    def _onchange_duedate_line_ids(self, values=False):
        self._compute_duedates_amounts()
    # end _onchange_duedate_line_ids

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
# end AccountMove
