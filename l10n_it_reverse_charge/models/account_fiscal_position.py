# Copyright 2021-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2021-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021-22 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#

from odoo import fields, models


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    # rc_type_id = fields.Many2one('account.rc.type', 'RC Type')

    rc_type = fields.Selection(
        selection=[
            ("", "No RC"),
            ("local", "RC locale"),
            ("self", "RC con autofattura"),
        ],
        string="Reverse charge",
        default="",
    )

    partner_type = fields.Selection(
        selection=[("supplier", "Fornitore"), ("other", "Azienda")],
        string="Tipo di Partner",
        default="",
    )

    self_journal_id = fields.Many2one(
        "account.journal",
        string="Registro per autofattura",
        domain=[("type", "=", "sale")],
        default="",
    )

    rc_fiscal_document_type_id = fields.Many2one(
        "fiscal.document.type",
        string="Self Invoice Fiscal Document Type",
    )
