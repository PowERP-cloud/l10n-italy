# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    rebate_active = fields.Many2one(
        related='company_id.rebate_active',
        string='Abbuono attivo',
        readonly=False,
    )

    rebate_passive = fields.Many2one(
        related='company_id.rebate_passive',
        string='Abbuono passivo',
        readonly=False,
    )

    rebate_delta = fields.Float(
        related='company_id.rebate_delta',
        string='Delta abbuono',
        readonly=False,
    )
