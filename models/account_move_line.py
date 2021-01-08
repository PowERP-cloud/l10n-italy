from odoo import models, api, fields
from odoo.exceptions import UserError

from ..utils import validate_selection


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    PAYMENT_METHODS_ALLOWED = [
        'invoice_financing',
        'riba_cbi',
        'sepa_direct_debit'
    ]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # INSOLUTO
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    @api.multi
    def open_wizard_insoluto(self):
        
        # Retrieve the records
        lines = self.env['account.move.line'].browse(self._context['active_ids'])
        
        # Perform validations
        validate_selection.same_payment_method(lines)
        validate_selection.assigned_to_payment_order(lines, assigned=True)
        validate_selection.same_payment_order(lines)
        validate_selection.allowed_payment_order_status(lines, ['done'])
        validate_selection.lines_has_payment(lines, paid=True)
        
        # Open the wizard
        wiz_view = self.env.ref(
            'account_banking_common.wizard_account_banking_common_insoluto'
        )
        return {
            'type': 'ir.actions.act_window',
            'name': 'Registra Insoluto',
            'res_model': 'wizard.account.banking.common.insoluto',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': wiz_view.id,
            'target': 'new',
            'res_id': False,
            'binding_model_id': 'account_banking_common.model_account_move_line',
            'context': {'active_ids': self._context['active_ids']},
        }
    # end validate_selection
    
    @api.multi
    def registra_insoluto(self):

        # The payment method of the selected lines
        p_method = self.get_payment_method()
        
        raise UserError(
            f'Procedura di registrazione insoluto non definita '
            f'per il metodo di pagamento {p_method.name}'
        )
    # end registra_insoluto
    
    @api.multi
    def registra_insoluto_standard(self):
        
        for r in self:

            # - - - - - - - - - - - - - - - - -
            # Retrieve the payment order data
            # - - - - - - - - - - - - - - - - -

            pol = r.payment_order_lines[0]  # Payment order line
            po = pol.order_id  # Payment order

            pol_partner = pol.partner_id  # Partner for this duedate
            po_journal = po.journal_id  # Journal selected in the po

            # - - - - - - - - - - - -
            # Accounts configuration
            # - - - - - - - - - - - -

            # account.account -> Bank
            acct_acct_bank_credit = po_journal.default_credit_account_id
            if not acct_acct_bank_credit:
                raise UserError(
                    f'Conto "avere" non configurato per non configurato per '
                    f'sezionale di banca '
                    f'{po_journal.display_name} ({po_journal.code})'
                )
            # end if

            # account.account -> Partner
            acct_acct_part = r.account_id

            # account.account -> Expenses
            acct_acct_expe = self.expenses_account

            # - - - - - - - - - - - - - -
            # New account.move creation
            # - - - - - - - - - - - - - -

            # 1 - Move lines

            if acct_acct_expe:

                # --> Spese addebitate al cliente
                if self.charge_client:

                    move_lines = [
                        # Banca c/c
                        {
                            'account_id': acct_acct_bank_credit.id,
                            'debit': 0, 'credit': r.debit + self.expenses_amount,
                        },

                        # Cliente
                        {
                            'account_id': acct_acct_part.id,
                            'partner_id': pol_partner.id,
                            'debit': r.debit + self.expenses_amount, 'credit': 0,
                        },
                    ]

                # --> Spese a nostro carico
                else:

                    move_lines = [
                        # Banca c/c
                        {
                            'account_id': acct_acct_bank_credit.id,
                            'debit': 0, 'credit': r.debit + self.expenses_amount,
                        },

                        # Spese bancarie
                        {
                            'account_id': acct_acct_expe.id,
                            'debit': self.expenses_amount, 'credit': 0
                        },

                        # Cliente
                        {
                            'account_id': acct_acct_part.id,
                            'partner_id': pol_partner.id,
                            'debit': r.debit, 'credit': 0,
                        },
                    ]

                # end if

            # --> Niente spese
            else:
                move_lines = [
                    # Banca c/c
                    {
                        'account_id': acct_acct_bank_credit.id,
                        'debit': 0, 'credit': r.debit
                    },

                    # Cliente
                    {
                        'account_id': acct_acct_part.id,
                        'partner_id': pol_partner.id,
                        'debit': r.debit, 'credit': 0,
                    },
                ]
            # end if

            # 2 - New account.move as draft
            # account_move = self.env['account.move'].create({
            self.env['account.move'].create({
                'type': 'entry',
                'date': fields.Date.today(),
                'journal_id': po_journal.id,
                'state': 'draft',
                'ref': 'Insoluto',
                'line_ids': [(0, 0, line) for line in move_lines],
            })

        # end for

    # end registra_insoluto_standard

    @api.multi
    def registra_accredito_standard(self):
        pass
    # end registra_accredito_standard


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # PAYMENT CONFIRM
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @api.multi
    def validate_payment_confirm(self):
        lines = self.env['account.move.line'].browse(
            self._context['active_ids'])

        # ----------------------------------------------------------------------
        # controlli
        # ----------------------------------------------------------------------

        # incasso effettuato deve essere False
        validate_selection.lines_has_payment(lines, paid=False)

        validate_selection.same_payment_method(lines)
        validate_selection.allowed_payment_method(lines,
                                                  self.PAYMENT_METHODS_ALLOWED)
        validate_selection.assigned_to_payment_order(lines, assigned=True)
        validate_selection.allowed_payment_order_status(lines, ['done'])
        validate_selection.same_payment_order(lines)

        # apertura wizard
        return {
            'type': 'ir.actions.act_window',
            'name': 'Conferma pagamento',
            'res_model': 'wizard.payment.order.confirm',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref(
                'account_banking_common.wizard_payment_order_confirm').id,
            'target': 'new',
            'res_id': False,
            'context': {'active_ids': self._context['active_ids']},
            "binding_model_id": "account.model_account_move_line"
        }
    # end validate_payment_confirm
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Metodi di utilità
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @api.multi
    def get_payment_method(self):
        return validate_selection.same_payment_method(self)
    # end get_payment_method_code

# end AccountMoveLine
