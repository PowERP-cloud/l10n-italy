from collections import defaultdict
from odoo import models, api
from odoo.exceptions import UserError

ALLOWED_PAYMENT_METHODS = [
    'sepa_direct_debit',
    'riba_cbi',
    'invoice_financing',
]


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.multi
    def validate_selection_insoluto(self):
        print('validate_selection!!')
        
        lines_set = self.env['account.move.line'].browse(self._context['active_ids'])
        for line in lines_set:
            print(f'\tmove line id:{line.id}')
        # end for

        return {
            'type': 'ir.actions.act_window',
            'name': 'FINESTRA DI TEST',
            'res_model': 'account.move.line',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'target': 'current',
            'res_id': False,
            "domain": [('id', 'in', self._context['active_ids'])]
        }
    # end validate_selection

    @api.multi
    def validate_payment_confirm(self):
        lines_set = self.env['account.move.line'].browse(
            self._context['active_ids'])

        payment_methods_allowed = ['invoice_financing', 'riba_cbi',
                                   'sepa_direct_debit']

        # ----------------------------------------------------------------------
        # controlli
        # ----------------------------------------------------------------------

        # conti e sezionale
        self._validate_config('invoice_financing')

        for line in lines_set:
            print(f'\tmove line id:{line.id}')

        # end for

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
            "domain": [('id', 'in', self._context['active_ids'])],
            "binding_model_id": "account.model_account_move_line"
        }
    # end validate_selection

    def _validate_config(self, payment_method_code):
        account_config = self.env['res.partner.bank'].get_payment_method_config(
            payment_method_code)
        config_errors = ''
        if not account_config['sezionale']:
            config_errors += "Non è stato impostato il registro per " \
                             "la registrazione contabile.\n"

        if not account_config['conto_effetti_attivi']:
            config_errors += "Non è stato impostato il conto effetti attivi.\n"

        if not account_config['banca_conto_effetti']:
            config_errors += "Non è stato impostato il conto " \
                             "'banca conto effetti'"
        if config_errors:
            config_errors = "Attenzione, configurazione incompleta\n\n" + \
                            config_errors
            raise UserError(config_errors)

# end AccountMoveLine
