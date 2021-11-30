# Copyright 2018-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import fields, models, api
from odoo.exceptions import UserError


class AccountPaymentMethod(models.Model):
    _inherit = 'account.payment.method'

    active = fields.Boolean('Active', default=True)

    debit_credit = fields.Selection(
        string='Debit / Credit',
        selection=[
            ('credit', 'Credit'),
            ('debit', 'Debit'),
        ],
        default=''
    )

    bank_account_required = fields.Boolean(
        string='Conto bancario necessario',
        default=False,
    )

    @api.model
    def get_payment_method_tax(self):
        res = self.search([('code', '=', 'tax')])

        if not res:
            raise UserError("Metodo di pagamento 'tax' non impostato")
        # end if

        return res[0]
    # end get_payment_method_tax


