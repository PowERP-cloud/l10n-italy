# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import models, api, fields
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountRegisterPayment(models.TransientModel):
    _name = 'wizard.account.register.payment'
    _description = 'Register payment from duedates tree view'

    def _set_sezionale(self):
        bank_account = self._get_bank_account()
        return bank_account.id

    journal_id = fields.Many2one(
        'account.journal',
        string='Registro',
        default=_set_sezionale,
    )

    registration_date = fields.Date(
        string='Data di registrazione',
        default=fields.Date.today()
    )

    def _get_bank_account(self):
        bank_account = self.env['res.partner.bank']
        lines = self.env['account.move.line'].browse(
            self._context['active_ids']
        )
        for line in lines:
            # Detect lines already reconciled
            if line.journal_id.id:
                bank_account = line.journal_id
                break
        return bank_account

    def register(self):

        if not self.journal_id.default_debit_account_id:
            raise UserError("Conto bancario dare di default nel registro "
                            "non impostato.")

        lines = self.env['account.move.line'].browse(
            self._context['active_ids']
        )

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
            'date': self.registration_date,
            'date_apply_vat': self.registration_date,
            'journal_id': self.journal_id.id,
            'type': 'entry',
            'ref': "Registrazione pagamento ",
            'state': 'draft',
        })

        move_id = self.env['account.move'].create(vals)

        move_line_model_no_check = \
            self.env['account.move.line'].with_context(
                check_move_validity=False)

        total_amount = 0.0

        for line in lines:
            total_amount += line.debit
            conto_dare = {
                'move_id': move_id.id,
                'account_id': line.account_id.id,
                'partner_id': line.partner_id.id,
                'credit': line.debit,
                'debit': 0
            }
            move_line_model_no_check.create(conto_dare)
        # end for

        conto_avere = {
            'move_id': move_id.id,
            'account_id': self.journal_id.default_debit_account_id.id,
            'credit': 0,
            'debit': total_amount
        }
        move_line_model_no_check.create(conto_avere)

        move_id.post()

