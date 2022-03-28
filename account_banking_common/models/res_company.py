#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    def _get_default_delta(self):
        return 1.0

    rebate_active = fields.Many2one(
        'account.account',
        string='Abbuono attivo',
        domain=[('nature', 'in', ['C', 'R'])],
    )

    rebate_passive = fields.Many2one(
        'account.account',
        string='Abbuono passivo',
        domain=[('nature', 'in', ['R', 'C'])],
    )

    rebate_delta = fields.Float(
        string='Delta abbuono',
        default=_get_default_delta,
    )

