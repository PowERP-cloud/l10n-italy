# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountTax(models.Model):
    _inherit = 'account.tax'

    @api.multi
    def _compute_rc(self):
        for tax in self:
            tax.rc_type = tax.check_rc()
        # end for

    # end _compute_rc

    rc_type = fields.Char('RC', compute='_compute_rc')

