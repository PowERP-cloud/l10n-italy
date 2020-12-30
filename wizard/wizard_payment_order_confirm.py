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

        payment_mode_id = self.env['account.payment.mode'].search([(
            'payment_method_code', '=', 'invoice_financing')])

        if self.account_expense and self.account_expense.id:
            if self.amount_expense > 0:
                amount_expense = self.amount_expense
        else:
            amount_expense = 0

        if len(active_ids) > 0:
            lines = self.env['account.move.line'].browse(active_ids)

            # 'child_ids': [
            #     (0, 0, categ1),
            #     (0, 0, categ2),
            # ]

            for line in lines:
                # partner
                partner_id = line.parner_id.id

                # banca
                bank = line.payment_line_ids.order_id.company_partner_bank_id

                # conti e sezionale
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

                line_ids = []

                if amount_expense > 0:
                    expense_move_line = {

                    }

                # tipo documento
                document_type = line.invoice_id.type
                if document_type in ['out_invoice']:
                    pass
                elif document_type in ['out_refund']:
                    pass


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

                account_move = self.env['account.move'].create(vals)

            return {'type': 'ir.actions.act_window_close'}
            # Aggiunta linee a distinta
            # TODO
            # lines.create_payment_line_from_move_line(payment_order)

            # Apertura ordine di pagamento
            # return {
            #     'type': 'ir.actions.act_window',
            #     'res_model': 'account.payment.order',
            #     'res_id': payment_order.id,
            #     'view_mode': 'form',
            #     'views': [(False, 'form')],
            #     'target': 'current',
            # }
        # end if
    # end confirm()

# end AccountPaymentGenerate
