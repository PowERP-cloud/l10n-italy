# Copyright 2021-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2021-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021-22 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
import logging

import odoo.addons.decimal_precision as dp
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    amount_rc = fields.Float(
        string="Iva RC",
        digits=dp.get_precision("Account"),
        readonly=True,
    )

    @api.multi
    @api.depends("line_ids.partner_id")
    def _compute_partner_id(self):
        """
        Override because of account move with lines which have
        different partners
        """
        super()._compute_partner_id()
        for move in self:
            if move.line_ids:
                lines = move.line_ids.filtered(lambda mv: mv.line_type == "lp")
                if lines:
                    invoice_id = lines[0].invoice_id
                    # partner_id = lines[0].partner_id
                    if (
                        invoice_id.fiscal_position_id
                        and invoice_id.fiscal_position_id.rc_type
                        and invoice_id.fiscal_position_id.rc_type == "self"
                    ):
                        move.partner_id = invoice_id.partner_id.id
                        _logger.info(
                            "move -> {mvid} parent_id > {pr}".format(
                                mvid=move.id, pr=move.partner_id.id
                            )
                        )
                    # end if
            # end if
        # end for

    # end _compute_partner_id
