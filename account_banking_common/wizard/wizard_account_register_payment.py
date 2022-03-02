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
        domain=[('is_wallet', '=', False), ('type', 'in', ('bank', 'cash'))],
        default=_set_sezionale,
    )

    registration_date = fields.Date(
        string='Data di registrazione',
        default=fields.Date.today()
    )

    def _get_bank_account(self):
        bank_account = self.env['account.journal']
        lines = self.env['account.move.line'].browse(
            self._context['active_ids']
        )
        for line in lines:
            # Detect lines already reconciled
            if line.company_bank_id.id:
                bank_account = line.company_bank_id.journal_id
                break
        return bank_account

    def register(self):

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Initial variables

        in_credit_total = 0
        in_debit_total = 0

        to_reconcile = list()

        move_line_model_no_check = self.env[
            'account.move.line'
        ].with_context(check_move_validity=False)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Retrieve lines
        selected_lines_ids = self._context['active_ids']
        lines = self.env['account.move.line'].browse(selected_lines_ids)

        # Identify the type of operation
        client_pay_reg = bool(len(
            [ln for ln in lines if ln.user_type_id.type == 'receivable']
        ))
        supplier_pay_reg = bool(len(
            [ln for ln in lines if ln.user_type_id.type == 'payable']
        ))

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Validity checks

        # Ensure than there are only client OR supplier lines but NOT BOTH
        if client_pay_reg and supplier_pay_reg:
            msg = (
                'Non è possibile creare un\'unica registrazione per '
                'registrare contemporaneamente pagamenti cliente e '
                'fornitore.\nUtilizzare la funzione di compensazione.'
            )
            raise UserError(msg)
        # end if

        assert client_pay_reg or supplier_pay_reg, (
            'Nessuna linea selezionata per l\'operazione '
            'di registrazione pagamento.'
        )

        # Ensure the required default account is set in the bank registry
        bank_line_account = None

        if client_pay_reg:

            bank_line_account = self.journal_id.default_debit_account_id

            if not (bank_line_account and bank_line_account.id):
                msg = 'Conto dare di default non impostato nel registro della banca.'
                raise UserError(msg)
            # end if

        elif supplier_pay_reg:

            bank_line_account = self.journal_id.default_credit_account_id

            if not(bank_line_account and bank_line_account.id):
                msg = 'Conto avere di default non impostato nel registro della banca.'
                raise UserError(msg)
            # end if

        # end if

        assert bank_line_account.id, (
            'Non è stato possibile identificare il conto da '
            'utilizzare per creare la move.line della banca.'
        )
        # end if

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Create the registration

        # Create the new account.move
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

        move = self.env['account.move'].create(vals)

        # For each input line add one line to the new account.move
        for in_line in lines:

            # Update totals
            in_credit_total += in_line.credit
            in_debit_total += in_line.debit

            # Create the new line with credit and debit swapped relative to the in_line
            new_line = move_line_model_no_check.create({
                'move_id': move.id,
                'account_id': in_line.account_id.id,
                'partner_id': in_line.partner_id.id,
                'credit': in_line.debit,
                'debit': in_line.credit,
            })

            # Reconciliation pair. The actual reconciliation will be performed
            # AFTER the confirmation (post() method call) of the new move.
            to_reconcile.append(in_line | new_line)
        # end for

        # Ensure we are not inverting the operation or
        # doing a pure reconciliation due to:
        #   - having mixed invoices and credit notes
        #   - total amount of credit notes >= total amount of invoices
        if client_pay_reg and not in_debit_total > in_credit_total:
            raise UserError(
                'L\'importo delle note di credito deve essere '
                'minore dell\'importo delle fatture cliente'
            )
        # end if

        if supplier_pay_reg and not in_credit_total > in_debit_total:
            raise UserError(
                'L\'importo delle note di credito deve essere '
                'minore dell\'importo delle fatture fornitore'
            )
        # end if

        # Create the bank line
        bank_line = move_line_model_no_check.create({
            'move_id': move.id,
            'account_id': bank_line_account.id,
            'credit': in_credit_total,
            'debit': in_debit_total,
        })

        # Confirm the account.move
        move.post()

        # Create reconciliations
        for pair in to_reconcile:
            pair.reconcile()
        # end if

        # TODO: riga inserita per debug, rimuovere a sviluppo completato
        print('Operation completed!!!!')
    # end register
# end AccountRegisterPayment
