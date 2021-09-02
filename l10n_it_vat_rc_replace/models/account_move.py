import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    @api.depends('line_ids.partner_id')
    def _compute_partner_id(self):
        """
        Override because of account move with lines which have
        different partners
        """

        for move in self:
            if move.line_ids:
                invoice_id = move.line_ids[0].invoice_id
                super()._compute_partner_id()
                if invoice_id.fiscal_position_id and \
                    invoice_id.fiscal_position_id.rc_type and \
                    invoice_id.fiscal_position_id.rc_type == 'self':
                    move.partner_id = invoice_id.partner_id
                # end if
            # end if
        # end for
    # end _compute_partner_id

