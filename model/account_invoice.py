# -*- coding: utf-8 -*-
#
# Copyright 2017-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#


from odoo import models, api, fields, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    duedate_ids = fields.One2many(
        string='Scadenze',
        comodel_name='account.move.line',
        related='move_id.duedate_ids',
        readonly=False,
    )
# end AccountInvoice
