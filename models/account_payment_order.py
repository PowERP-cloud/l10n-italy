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
