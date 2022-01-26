#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import api, fields


class BaseMixin:

    def _counterparty_bank_id_domain(self):
        # Variabile separata per facilitare debug
        domain = [('partner_id', '=', self.partner_id.id)]
        return domain
    # end _counterparty_bank_id_domain

    def _company_bank_id_domain(self):
        # Variabile separata per facilitare debug
        domain = [
            ('partner_id', '=', self.env.user.company_id.partner_id.id),
            ('bank_is_wallet', '=', False)
        ]

        return domain
    # end _company_bank_id_domain

    counterparty_bank_id = fields.Many2one(
        string="Banca d'appoggio",
        comodel_name='res.partner.bank',
        domain=_counterparty_bank_id_domain,
        copy=True,
    )

    company_bank_id = fields.Many2one(
        string='Banca aziendale',
        comodel_name='res.partner.bank',
        domain=_company_bank_id_domain,
        copy=True,
    )


