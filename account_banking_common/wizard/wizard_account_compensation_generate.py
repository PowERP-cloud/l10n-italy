# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import models, api, fields

_logger = logging.getLogger(__name__)


class AccountCompensationGenerate(models.TransientModel):
    _name = 'wizard.account.compensation.generate'
    _description = 'Create compensation from duedates tree view'

    def _set_same_account(self):
        return self._context['same_account']

    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
    )

    compensation_date = fields.Date(
        string='Data di registrazione',
    )

    compensation_amount = fields.Float(
        string='Importo di compensazione',
    )

    same_account = fields.Boolean(
        string='Stesso conto',
        default=_set_same_account
    )

    def compensate(self):
        # lines = self.env['account.move.line'].browse(
        #     self._context['active_ids']
        # )

        lines = self.env['account.move.line'].search(
            [('id', 'in', self._context['active_ids'])],
            order='date_maturity asc')

        if self._context.get('same_account'):
            # nothing to do only reconcile
            lines.reconcile()
        else:

            debit_amount = 0
            credit_amount = 0

            for line in lines:
                debit_amount += line.debit
                credit_amount += line.credit

            if debit_amount > credit_amount:
                compensation_base = credit_amount
                comp_unit = 'credit'
            elif credit_amount > debit_amount:
                compensation_base = debit_amount
                comp_unit = 'debit'
            else:
                compensation_base = credit_amount
                comp_unit = 'credit'

            vals = self.env['account.move'].default_get([
                'date_effective',
                'fiscalyear_id',
                'invoice_date',
                'narration',
                'payment_term_id',
                'reverse_date',
                'tax_type_domain',
            ])

            vals.update({
                'date': self.compensation_date,
                'date_apply_vat': self.compensation_date,
                'journal_id': self.journal_id.id,
                'type': 'entry',
                'ref': "Compensazione ",
                'state': 'draft',
            })
            # Creazione registrazione contabile

            move_id = self.env['account.move'].create(vals)

            totally_compensate = dict()

            if comp_unit == 'credit':
                tot_compensate_lines = lines.filtered(
                    lambda x: x.credit > 0
                )
                tot_compensate_left = lines.filtered(
                    lambda x: x.debit > 0
                )
            else:
                tot_compensate_lines = lines.filtered(
                    lambda x: x.debit > 0
                )
                tot_compensate_left = lines.filtered(
                    lambda x: x.credit > 0
                )

            for line in tot_compensate_lines:
                v = {
                    'partner_id': line.partner_id.id,
                    'account_id': line.account_id.id,
                    'debit': line.credit if comp_unit == 'credit' else 0,
                    'credit': line.debit if comp_unit == 'debit' else 0,
                    'move_id': move_id.id,
                }
                totally_compensate.update({
                    line.id: v
                })

            for line in tot_compensate_left:
                pass

            # move_line_model_no_check = self.env['account.move.line'].with_context(
            #     check_move_validity=False
            # )

        # end if

