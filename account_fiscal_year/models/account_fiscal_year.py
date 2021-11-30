# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# from datetime import datetime
# from dateutil.relativedelta import relativedelta
# import odoo
from odoo import models, fields
# from odoo.osv import expression


class AccountFiscalyear(models.Model):
    _inherit = "account.fiscal.year"

    state = fields.Selection([('draft', 'Open'),
                              ('done', 'Closed')],
                             'Status', copy=False,
                             default='draft')
