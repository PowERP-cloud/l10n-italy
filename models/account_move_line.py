from odoo import models, api


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

        # controlli
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

# end AccountMoveLine
