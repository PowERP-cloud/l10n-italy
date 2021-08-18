# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = "account.journal"

    portafolio_account = fields.Boolean(string="Ritenuta d'acconto", default=False)

    portafolio_childs = fields.One2many(
        comodel_name='account.journal',
        inverse_name='portafolio_parent_id',
        string='Conti di portafoglio',
        domain=[('type', 'in', ['bank', 'cash']),
                ('portafolio_account', '=', False)]
    )

    portafolio_parent_id = fields.Many2one(
        comodel_name='account.journal',
        string='Conto padre')

