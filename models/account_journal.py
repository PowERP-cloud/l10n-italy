# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = "account.journal"

    def _set_portafolio_parent_default(self):
        return self.env['account.journal']
    # end _set_portafolio_parent_default

    def _set_portafolio_childs_default(self):
        domain = [
            ('type', 'in', ['bank', 'cash']),
            ('portafolio_account', '=', True),
            ('portafolio_parent_id', '=', self.id)]

        return self.search(domain)
    # end _set_portafolio_childs_default

    @api.depends('portafolio_childs')
    def _has_children(self):
        if self.portafolio_childs:
            self.has_children = True
        else:
            self.has_children = False
        # end if
    # end _has_children

    portafolio_account = fields.Boolean(string="Conto di portafoglio",
                                        default=False)

    portafolio_childs = fields.One2many(
        comodel_name='account.journal',
        inverse_name='portafolio_parent_id',
        string='Conti di portafoglio',
        default=_set_portafolio_childs_default,
        readonly=True,
    )

    portafolio_parent_id = fields.Many2one(
        comodel_name='account.journal',
        string='Conto padre',
        domain=[('type', 'in', ['bank', 'cash']),
                ('portafolio_account', '=', False),
                ],
        default=_set_portafolio_parent_default
    )

    has_children = fields.Boolean(
        string="Conto padre",
        compute='_has_children'
        )

    @api.onchange('portafolio_account')
    def _on_change_portafolio_account(self):
        if not self.portafolio_account:
            # empty parent
            if self.portafolio_parent_id:
                self.portafolio_parent_id = self._set_portafolio_parent_default()
            # end if
        # end if
    # end _on_change_portafolio_account

