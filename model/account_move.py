#
# Copyright 2020 - Didotech s.r.l. <https://www.didotech.com/>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#


from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    duedate_ids = fields.One2many(
        string='Scadenze',
        comodel_name='account.move.line',
        inverse_name='move_id_duedate',
    )
# end AccountMove
