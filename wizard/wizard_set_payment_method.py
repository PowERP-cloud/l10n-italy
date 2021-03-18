import logging
from odoo import models, api, fields
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WizardSetPaymentMethod(models.TransientModel):
    _name = 'wizard.set.payment.method'
    _description = 'Set or update payment mathod into due dates'

    payment_method = fields.Many2one('account.payment.method',
                                     string="Metodo di pagamento",
                                     required=True,
                                     default=False
                                     )

    overwrite = fields.Boolean(string='Sovrascrivi', default=False)

    @api.multi
    def update_duedates(self):
        active_ids = self._context.get('active_ids')
        if len(active_ids) > 0:
            lines = self.env['account.move.line'].browse(active_ids)
            for line in lines:
                up = line.payment_method.id and self.overwrite or True
                if up:
                    line.write({
                        'payment_method':  self.payment_method.id
                    })

        return {'type': 'ir.actions.act_window_close'}

    # end update_duedates

# end WizardSetPaymentMethod
