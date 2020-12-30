from odoo import models, api
from ..utils import validate_selection


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    INSOLUTO_PM = ['riba_cbi', 'sepa_direct_debit']

    PAYMENT_METHODS_ALLOWED = ['invoice_financing', 'riba_cbi',
                               'sepa_direct_debit']

    @api.multi
    def open_wizard_insoluto(self):
        
        # Retrieve the records
        lines = self.env['account.move.line'].browse(self._context['active_ids'])
        
        # Perform validations
        validate_selection.same_payment_method(lines)
        validate_selection.allowed_payment_method(lines, self.INSOLUTO_PM)
        validate_selection.assigned_to_payment_order(lines, assigned=True)
        validate_selection.allowed_payment_order_status(lines, ['uploaded'])
        
        # Open the wizard
        return {
            'type': 'ir.actions.act_window',
            'name': 'Registra Insoluto',
            'res_model': 'wizard.account.banking.common.insoluto',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'target': 'new',
            'res_id': False,
            'binding_model_id': 'account_banking_common.model_account_move_line',
            'context': {'active_ids': self._context['active_ids']},
        }
    # end validate_selection

    @api.multi
    def validate_payment_confirm(self):
        lines = self.env['account.move.line'].browse(
            self._context['active_ids'])

        # ----------------------------------------------------------------------
        # controlli
        # ----------------------------------------------------------------------

        # conti e sezionale
        # self._validate_config('invoice_financing')

        # restanti controlli
        validate_selection.same_payment_method(lines)
        validate_selection.allowed_payment_method(lines,
                                                  self.PAYMENT_METHODS_ALLOWED)
        validate_selection.assigned_to_payment_order(lines, assigned=True)
        validate_selection.except_payment_order_status(lines, ['done'])
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
            "domain": [('id', 'in', self._context['active_ids'])],
            "binding_model_id": "account.model_account_move_line"
        }
    # end validate_selection

# end AccountMoveLine
