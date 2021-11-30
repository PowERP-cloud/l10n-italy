# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountTax(models.Model):
    _inherit = 'account.tax'

    def check_rc(self):
        value = ''
        if self.kind_id:
            if self.kind_id.code.startswith('N3'):
                if self.kind_id.code != 'N3.5':
                    value = 'local'
                # end if
            elif self.kind_id.code.startswith('N6'):
                value = 'self'
            # end if
        # end if

        return value
    # end check_rc


