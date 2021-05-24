# Copyright (c) 2020
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
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
    lines_count = fields.Integer(compute='count_line_ids')
