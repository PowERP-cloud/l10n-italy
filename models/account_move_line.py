from odoo import fields, models, api


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
# end AccountMoveLine
