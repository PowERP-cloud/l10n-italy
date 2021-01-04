#
# Copyright 2017-20 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Copyright 2020 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import logging
from odoo import models, api, fields
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WizardPaymentOrderConfirm(models.TransientModel):
    _name = 'wizard.payment.order.confirm'
    _description = 'Create confirm payment wizard from due dates tree view'

    account_expense = fields.Many2one(
        'account.account',
        string='Conto spese',
        domain=[(
            'internal_group', '=', 'expense')]
    )

    amount_expense = fields.Float(string='Importo', )

    @api.multi
    def confirm(self):

        active_ids = self._context.get('active_ids')

        # Debug - begin
        print('Active ids:', active_ids)
        # Debug - end

        if self.account_expense and self.account_expense.id:
            if self.amount_expense > 0:
                amount_expense = self.amount_expense
        else:
            amount_expense = 0

        if len(active_ids) > 0:
            lines = self.env['account.move.line'].browse(active_ids)

            for line in lines:

                # CONFIG
                #   banca
                bank = line.payment_line_ids.order_id.company_partner_bank_id
                #   conti e sezionale
                account_config = bank.get_payment_method_config(
                    'invoice_financing')

                # validazione conti e sezionale
                config_errors = ''
                if not account_config['sezionale']:
                    config_errors += "Non è stato impostato il registro per " \
                                     "la registrazione contabile.\n"

                if not account_config['conto_effetti_attivi']:
                    config_errors += "Non è stato impostato il conto " \
                                     "effetti attivi.\n"

                if not account_config['banca_conto_effetti']:
                    config_errors += "Non è stato impostato il conto " \
                                     "'banca conto effetti'"
                if config_errors:
                    config_errors = "Attenzione, configurazione " \
                                    "incompleta\n\n" + \
                                    config_errors
                    raise UserError(config_errors)

                # per ogni riga
                # genero una registrazione

                line_ids = []

                # tipo documento
                document_type = line.invoice_id.type

                # - Avere / credit -> Banca Conto Effetti + partner
                # per importo della scadenza(attenzione a NC, il segno
                # dare/avere è opposto alla registrazione di account.move.line)

                # - Dare / debit -> Conto Effetti Attivi
                # con il totale delle righe precedenti(attenzione
                # ai segni)

                # se fattura
                if document_type in ['out_invoice']:

                    # se ci sono spese le aggiungo
                    if amount_expense > 0:
                        expense_move_line = {
                            'account_id': self.account_expense.id,
                            'credit': 0,
                            'debit': amount_expense,
                        }
                        line_ids.append((0, 0, expense_move_line))

                    # banca conto effetti
                    banca_conto_effetti = {
                        'account_id': account_config['banca_conto_effetti'].id,
                        'partner_id': line.partner_id.id,
                        'credit': line.debit,
                        'debit': 0,
                    }
                    line_ids.append((0, 0, banca_conto_effetti))

                    conto_effetti_attivi = {
                        'account_id': account_config['conto_effetti_attivi'].id,
                        'credit': 0,
                        'debit': line.debit - amount_expense
                    }
                    line_ids.append((0, 0, conto_effetti_attivi))

                # se Nota di Credito
                elif document_type in ['out_refund']:

                    # se ci sono spese le aggiungo
                    if amount_expense > 0:
                        expense_move_line = {
                            'account_id': self.account_expense.id,
                            'credit': 0,
                            'debit': amount_expense,
                        }
                        line_ids.append((0, 0, expense_move_line))

                    # banca conto effetti
                    banca_conto_effetti = {
                        'account_id': account_config['banca_conto_effetti'].id,
                        'partner_id': line.partner_id.id,
                        'credit': 0,
                        'debit': line.credit,
                    }
                    line_ids.append((0, 0, banca_conto_effetti))

                    conto_effetti_attivi = {
                        'account_id': account_config['conto_effetti_attivi'].id,
                        'credit': line.credit + amount_expense,
                        'debit': 0
                    }
                    line_ids.append((0, 0, conto_effetti_attivi))

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
                    'journal_id': account_config['sezionale'].id,
                    'type': 'entry',
                    'ref': "Conferma pagamento ",
                    'state': 'draft',
                    'line_ids': line_ids
                })
                # Creazione registrazione contabile

                self.env['account.move'].create(vals)

            return {'type': 'ir.actions.act_window_close'}
        # end if
    # end confirm()

# end AccountPaymentGenerate
