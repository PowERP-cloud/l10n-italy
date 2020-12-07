#
# Copyright (c) 2020
#
import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    @api.depends('line_ids')
    def count_line_ids(self):
        for rec in self:
            rec.lines_count = len(rec.line_ids)
        # end for
    # end def

    fiscalyear_id = fields.Many2one('account.fiscal.year',
                                    string="Esercizio contabile")

    date_apply_balance = fields.Date(
        string='Data competenza',
    )

    lines_count = fields.Integer(compute='count_line_ids')
