#
# Copyright 2017-20 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Copyright 2020 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import logging
from odoo import models, api, fields

_logger = logging.getLogger(__name__)


class WizardPaymentOrderCredit(models.TransientModel):
    _name = 'wizard.payment.order.credit'

    account_expense = fields.Many2one(
        'account.account',
        string='Conto spese',
        domain=[(
            'internal_group', '=', 'expense')]
    )

    amount_expense = fields.Float(string='Importo', )

    @api.multi
    def registra_accredito(self):
        '''Create on new account.move for each line of payment order'''

        model = self.env['account.payment.order']
        recordset = model.browse(self._context['active_id'])
        recordset.registra_accredito()

        return {'type': 'ir.actions.act_window_close'}

    # end registra_insoluto

    # @api.multi
    # def confirm(self):
    #
    #     # ordine che voglio accreditare
    #     active_id = self._context.get('active_id')
    #
    #     # Debug - begin
    #     print('Active id:', active_id)
    #     # Debug - end
    #
    #     # spese qualora ce ne siano
    #     if self.account_expense and self.account_expense.id:
    #         if self.amount_expense > 0:
    #             amount_expense = self.amount_expense
    #     else:
    #         amount_expense = 0
    #
    #     if active_id:
    #
    #         sezionale = False
    #
    #         payment_order = self.env['account.payment.order'].browse(active_id)
    #
    #         # conto di compensazione / effetti salvo buon fine
    #         check_offsetting_account = payment_order.payment_mode_id.\
    #             offsetting_account
    #
    #         if check_offsetting_account == 'bank_account':
    #             raise UserError("Attenzione!\nConto di trasferimento non "
    #                             "impostato.")
    #         elif check_offsetting_account == 'transfer_account':
    #             offsetting_account = payment_order.payment_mode_id.\
    #                 transfer_account_id
    #             sezionale = payment_order.payment_mode_id.transfer_journal_id
    #
    #         # spese banca
    #         bank_account = payment_order.journal_id. \
    #             default_credit_account_id
    #
    #         if not bank_account.id:
    #             raise UserError("Attenzione!\nConto banca non impostato.")
    #
    #         # CONFIG
    #         #   banca
    #         bank = payment_order.company_partner_bank_id
    #         #   conti e sezionale
    #         account_config = bank.get_payment_method_config(
    #             payment_order.payment_method_code)
    #
    #         # validazione conti e sezionale
    #         config_errors = ''
    #
    #         if not account_config['banca_conto_effetti']:
    #             config_errors += "Non è stato impostato il conto " \
    #                              "'banca conto effetti'"
    #         if config_errors:
    #             config_errors = "Attenzione, configurazione " \
    #                             "incompleta\n\n" + \
    #                             config_errors
    #             raise UserError(config_errors)
    #
    #         lines = self.env['account.payment.line'].search(
    #             [('order_id', '=', active_id)])
    #
    #         for line in lines:
    #
    #             # per ogni riga
    #             # genero una registrazione
    #
    #             line_ids = []
    #
    #             # se ci sono spese le aggiungo
    #             if amount_expense > 0:
    #                 expense_move_line = {
    #                     'account_id': self.account_expense.id,
    #                     'credit': 0,
    #                     'debit': amount_expense,
    #                 }
    #                 line_ids.append((0, 0, expense_move_line))
    #
    #                 bank_expense_line = {
    #                     'account_id': bank_account.id,
    #                     'credit': amount_expense,
    #                     'debit': 0,
    #                 }
    #                 line_ids.append((0, 0, bank_expense_line))
    #
    #             # banca conto effetti
    #             banca_conto_effetti = {
    #                 'account_id': account_config['banca_conto_effetti'].id,
    #                 'partner_id': line.partner_id.id,
    #                 'credit': 0,
    #                 'debit': line.amount_currency,
    #             }
    #             line_ids.append((0, 0, banca_conto_effetti))
    #
    #             effetti_attivi = {
    #                 'account_id': offsetting_account.id,
    #                 'credit': line.amount_currency,
    #                 'debit': 0
    #             }
    #             line_ids.append((0, 0, effetti_attivi))
    #
    #             vals = self.env['account.move'].default_get([
    #                 'date_apply_balance',
    #                 'date_effective',
    #                 'fiscalyear_id',
    #                 'invoice_date',
    #                 'narration',
    #                 'payment_term_id',
    #                 'reverse_date',
    #                 'tax_type_domain',
    #             ])
    #             vals.update({
    #                 'date': fields.Date.today(),
    #                 'date_apply_vat': fields.Date.today(),
    #                 'journal_id': sezionale.id,
    #                 'type': 'entry',
    #                 'ref': "Accreditamento ",
    #                 'state': 'draft',
    #                 'line_ids': line_ids
    #             })
    #
    #             # Creazione registrazione contabile
    #             self.env['account.move'].create(vals)
    #
    #         payment_order.action_done()
    #
    #         return {'type': 'ir.actions.act_window_close'}
    #     # end if
    # # end confirm()

# end AccountPaymentGenerate
