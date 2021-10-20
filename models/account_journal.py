# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import api, fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    def _set_main_bank_account_id_default(self):
        return self.env['account.journal']

    # end _set_main_bank_account_id_default

    def _set_wallet_ids_default(self):
        domain = [
            ('type', 'in', ['bank', 'cash']),
            ('is_wallet', '=', True),
            ('main_bank_account_id', '=', self.id),
        ]

        return self.search(domain)

    # end _set_wallet_ids_default

    def is_wallet_default(self):
        if self.bank_account_id:
            return self.bank_account_id.bank_is_wallet
        else:
            return False
        # end if

    # end is_wallet_default

    @api.depends('wallet_ids')
    def _has_children(self):
        if self.wallet_ids:
            self.has_children = True
        else:
            self.has_children = False
        # end if

    # end _has_children

    is_wallet = fields.Boolean(string="Conto di portafoglio", default=is_wallet_default)

    wallet_ids = fields.One2many(
        comodel_name='account.journal',
        inverse_name='main_bank_account_id',
        string='Conti di portafoglio',
        default=_set_wallet_ids_default,
        readonly=True,
    )

    main_bank_account_id = fields.Many2one(
        comodel_name='account.journal',
        string='Conto padre',
        domain=[
            ('type', 'in', ['bank', 'cash']),
            ('is_wallet', '=', False),
        ],
        default=_set_main_bank_account_id_default,
    )

    has_children = fields.Boolean(string="Conto padre", compute='_has_children')

    @api.onchange('is_wallet')
    def _on_change_is_wallet(self):
        if not self.is_wallet:
            # empty parent
            if self.main_bank_account_id:
                self.main_bank_account_id = self._set_main_bank_account_id_default()
            # end if
        # end if
        if self.bank_account_id:
            bank_account = self.env['res.partner.bank'].browse(self.bank_account_id.id)
            bank_account.write({'bank_is_wallet': self.is_wallet})
        # end if

    # end _on_change_portafolio_account
