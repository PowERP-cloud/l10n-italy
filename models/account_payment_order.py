#
# Copyright (c) 2021
#
from odoo import models, api, fields
from odoo.exceptions import UserError


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    @api.multi
    def action_accreditato(self):

        for order in self:
            if order.state == 'uploaded':
                # validation
                if order.payment_mode_id.payment_method_code not in [
                    'invoice_financing', 'riba_cbi', 'sepa_direct_debit'
                ]:
                    raise UserError('Attenzione!\nIl metodo di pagamento non '
                                    'permette l\'accreditamento.')

                # apertura wizard
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Accreditamento',
                    'res_model': 'wizard.payment.order.credit',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'view_id': self.env.ref(
                        'account_banking_common.wizard_payment_order_credit').id,
                    'target': 'new',
                    'res_id': False,
                    "binding_model_id": "account.model_account_payment_order"
                }

    @api.multi
    def registra_accredito(self):
        # The payment method of the selected lines
        raise UserError(
            f'Procedura di registrazione accredito non definita '
            f'per il metodo di pagamento {self.payment_mode_id.name}'
        )
    # end registra_accredito_standard

    @api.multi
    def registra_accredito_standard(self):

        account_expense_id = self._context.get('expenses_account_id')
        amount_expense = self._context.get('expenses_amount')

        for payment_order in self:

            # impostazione sezionale dal conto di compensazione
            sezionale = False

            # conto di compensazione / effetti salvo buon fine
            check_offsetting_account = payment_order.payment_mode_id. \
                offsetting_account

            if check_offsetting_account == 'bank_account':
                raise UserError("Attenzione!\nConto di trasferimento non "
                                "impostato.")
            elif check_offsetting_account == 'transfer_account':
                offsetting_account = payment_order.payment_mode_id. \
                    transfer_account_id
                sezionale = payment_order.payment_mode_id.transfer_journal_id

            # spese banca
            bank_account = payment_order.journal_id. \
                default_credit_account_id

            if not bank_account.id:
                raise UserError("Attenzione!\nConto banca non impostato.")

            # CONFIG
            #   banca
            bank = payment_order.company_partner_bank_id
            #   conti e sezionale
            account_config = bank.get_payment_method_config(
                payment_order.payment_method_code)

            # validazione conti e sezionale
            config_errors = ''

            if not account_config['banca_conto_effetti']:
                config_errors += "Non è stato impostato il conto " \
                                 "'banca conto effetti'"
            if config_errors:
                config_errors = "Attenzione, configurazione " \
                                "incompleta\n\n" + \
                                config_errors
                raise UserError(config_errors)

            lines = self.env['account.payment.line'].search(
                [('order_id', '=', payment_order.id)])

            for line in lines:

                # per ogni riga
                # genero una registrazione

                line_ids = []

                # se ci sono spese le aggiungo
                if amount_expense > 0:
                    expense_move_line = {
                        'account_id': account_expense_id,
                        'credit': 0,
                        'debit': amount_expense,
                    }
                    line_ids.append((0, 0, expense_move_line))

                    bank_expense_line = {
                        'account_id': bank_account.id,
                        'credit': amount_expense,
                        'debit': 0,
                    }
                    line_ids.append((0, 0, bank_expense_line))

                # banca conto effetti
                banca_conto_effetti = {
                    'account_id': account_config['banca_conto_effetti'].id,
                    'partner_id': line.partner_id.id,
                    'credit': 0,
                    'debit': line.amount_currency,
                }
                line_ids.append((0, 0, banca_conto_effetti))

                effetti_attivi = {
                    'account_id': offsetting_account.id,
                    'credit': line.amount_currency,
                    'debit': 0
                }
                line_ids.append((0, 0, effetti_attivi))

                vals = self.env['account.move'].default_get([
                    'date_apply_balance',
                    'date_effective',
                    'fiscalyear_id',
                    'invoice_date',
                    'narration',
                    'payment_term_id',
                    'reverse_date',
                    'tax_type_domain',
                ])
                vals.update({
                    'date': fields.Date.today(),
                    'date_apply_vat': fields.Date.today(),
                    'journal_id': sezionale.id,
                    'type': 'entry',
                    'ref': "Accreditamento ",
                    'state': 'draft',
                    'line_ids': line_ids
                })

                # Creazione registrazione contabile
                self.env['account.move'].create(vals)

            payment_order.action_done()

    # end registra_accredito_standard

    @api.multi
    def unlink(self):
        
        for order in self:
            if order.state != 'cancel':
                raise UserError(
                    f'L\'ordine di pagamento {order.name} non può essere'
                    f'eliminato perché non è nello stato "Annullato"'
                )
            # end if
        # end for
        
        return super(AccountPaymentOrder, self).unlink()
    # end unlink
# end AccountPaymentOrder
