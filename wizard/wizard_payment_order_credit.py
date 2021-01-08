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
        recordset.with_context({
            'expenses_account_id': self.account_expense.id,
            'expenses_amount': self.amount_expense,
        }).registra_accredito()

        return {'type': 'ir.actions.act_window_close'}

    # end registra_accredito

# end AccountPaymentGenerate
