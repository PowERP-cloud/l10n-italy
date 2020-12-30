#
# Copyright 2017-20 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Copyright 2020 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import logging
from collections import defaultdict
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

        account_config = self.env['res.partner.bank'].get_payment_method_config(
            'invoice_financing')
        payment_mode_id = self.env['account.payment.mode'].search([(
            'payment_method_code', '=', 'invoice_financing')])

        if len(active_ids) > 0:

            lines = self.env['account.move.line'].browse(active_ids)

            # Check for errors
            self._raise_on_errors(lines)

            # Creazione distinta
            payment_order = self.env['account.payment.order'].create({
                'payment_mode_id': payment_mode_id.id,
                'journal_id': account_config['sezionale'].id,
                'description': '',
            })

            # Aggiunta linee a distinta
            # TODO
            # lines.create_payment_line_from_move_line(payment_order)

            # Apertura ordine di pagamento
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.payment.order',
                'res_id': payment_order.id,
                'view_mode': 'form',
                'views': [(False, 'form')],
                'target': 'current',
            }
        # end if
    # end generate()

    @api.model
    def _raise_on_errors(self, lines):
        not_busy_lines = list()
        payment_methods = defaultdict(lambda: {'count': 0, 'name': None})

        for line in lines:

            # Detect lines already assigned to a payment order
            if not line.payment_line_ids:
                not_busy_lines.append(line)
            # end if

            # Check same payment method
            if line.payment_method:
                payment_methods[line.payment_method.id]['count'] += 1
                payment_methods[line.payment_method.id]['name'] = line.payment_method.name
            else:
                payment_methods[-1]['count'] += 1
                payment_methods[-1]['name'] = 'Non impostato'
        # end for

        error_not_busy = len(not_busy_lines) > 0
        error_method = len(payment_methods) > 1

        if error_not_busy or error_method:

            error_msg_busy = ''
            if error_not_busy:
                error_msg_busy = self._error_msg_busy(not_busy_lines)
            # end if

            error_msg_method = ''
            if error_method:
                error_msg_method = self._error_msg_method(payment_methods)
            # end if

            # Separate error messages with two newlines if both error
            # messages should be displayed
            error_msg_busy += (error_not_busy and error_method and '\n\n\n') or ''

            raise UserError(error_msg_busy + error_msg_method)
        # end if
    # end _check_for_errors

    @staticmethod
    def _error_msg_busy(busy_lines):
        msg = 'ATTENZIONE!\nLe seguenti righe' \
              ' non sono parte di una distinta:\n\n - '

        msg += '\n - '.join(
            map(
                lambda x: x.invoice_id.number + '    ' + str(x.date_maturity),
                busy_lines
            )
        )

        return msg
    # end _error_msg_busy

    @staticmethod
    def _error_msg_method(payment_methods):
        msg = 'ATTENZIONE!\nSono state selezionate righe' \
              ' con più metodi di pagamento:\n\n - '

        msg += '\n - '.join(
            map(
                lambda x: x['name'],
                payment_methods.values()
            )
        )

        return msg
    # end _error_msg_method
# end AccountPaymentGenerate
