# Copyright 2021-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2021-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021-22 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    rev_charge = fields.Boolean(
        "Reverse Charge journal",
        default=False,
        help=(
            "Set to True if this journal "
            "is used to store reverse-charge self-invoices"
        ),
    )
