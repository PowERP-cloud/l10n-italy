#
# Copyright (c) 2021
#
from odoo import models, api, fields
from odoo.exceptions import UserError


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    payment_method_code = fields.Char(
        string='Codice metodo di pagamento',
        related='payment_method_id.code',
    )

    @api.multi
    def action_accreditato(self):

        for order in self:
            if order.state == 'uploaded':
                # validation
                if order.payment_method_code not in [
                    'riba_cbi', 'sepa_direct_debit'
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
    # end registra_accredito

    @api.multi
    def registra_accredito_standard(self):

        account_expense_id = self._context.get('expenses_account_id')
        amount_expense = self._context.get('expenses_amount')

        for payment_order in self:

            cfg = payment_order.get_move_config()

            # validazione conti impostati

            if not cfg['sezionale'].id:
                raise UserError("Attenzione!\nSezionale non "
                                "impostato.")

            if not cfg['effetti_allo_sconto'].id:
                raise UserError("Attenzione!\nConto effetti allo sconto "
                                "non impostato.")

            if not cfg['bank_journal'].id:
                raise UserError("Attenzione!\nConto di costo non impostato.")

            bank_account = cfg['bank_journal'].default_credit_account_id

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
                # end if

                # conto effetti allo sconto
                effetti_allo_sconto = {
                    'account_id': cfg['effetti_allo_sconto'].id,
                    'credit': 0,
                    'debit': line.amount_currency,
                }
                line_ids.append((0, 0, effetti_allo_sconto))

                effetti_attivi = {
                    'account_id': cfg['conto_effetti_attivi'].id,
                    'partner_id': line.partner_id.id,
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
                    'journal_id': cfg['sezionale'].id,
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

    @api.model
    def get_move_config(self):
        '''Returns the journals and accounts to be used for creating new account.move records'''

        po = self
        pay_mode = po.payment_mode_id
        pay_method = po.payment_method_id
        res_bank_acc = po.company_partner_bank_id

        # 1 - Get default config from res_bank_account
        cfg = res_bank_acc.get_payment_method_config(pay_method.code)

        # 2 - Get overrides from payment mode
        if pay_mode.offsetting_account == 'transfer_account':
            assert pay_mode.transfer_journal_id.id
            cfg['transfer_journal'] = pay_mode.transfer_journal_id
            cfg['sezionale'] = cfg['transfer_journal']

            assert pay_mode.transfer_account_id.id
            cfg['transfer_account'] = pay_mode.transfer_account_id
            cfg['conto_effetti_attivi'] = cfg['transfer_account']
        # end if

        # 3 - Add bank journal
        cfg['bank_journal'] = po.journal_id

        return cfg
    # end get_move_config
# end AccountPaymentOrder
