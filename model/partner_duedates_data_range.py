#
# Copyright 2020 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#

from odoo import models, api, fields
from odoo.exceptions import UserError


class PartnerDuedatesDatarange(models.Model):
    _name = "partner.duedates.datarange"

    partner_id = fields.Many2one(
        string='Partner',
        comodel_name='res.partner',
        required=False,
    )

    period_id = fields.Many2one(
        string='Periodo',
        comodel_name='date.range',
        required=True,
        domain=[('active', '=', True)]
    )

    split_date = fields.Date(
        string='Data di slittamento',
        required=True,
        default=False
    )

    enable_customer = fields.Boolean(string='Abilita cliente', default=False)
    enable_supplier = fields.Boolean(string='Abilita fornitore', default=False)

    @api.model
    def create(self, values):
        if values['split_date']:
            data_range = self.env['date.range'].browse(values['period_id'])
            df = data_range.date_end.strftime('%d/%m/%Y')
            comparison_date = fields.Date.from_string(values['split_date'])
            if comparison_date <= data_range.date_end:
                raise UserError('La data di slittamento deve essere '
                                'maggiore del periodo che ha data di '
                                'fine {df}!'.format(df=df))
            else:
                return super().create(values)
        # end if
    # end create

    @api.multi
    def write(self, values):
        if 'split_date' in values and values['split_date']:
            if 'period_id' in values and values['period_id']:
                data_range = self.env['date.range'].browse(values['period_id'])
            else:
                data_range = self.period_id
            df = data_range.date_end.strftime('%d/%m/%Y')
            comparison_date = fields.Date.from_string(values['split_date'])
            if comparison_date <= data_range.date_end:
                raise UserError('La data di slittamento deve essere '
                                'maggiore del periodo che ha data di '
                                'fine {df}!'.format(df=df))
            else:
                return super().write(values)
        # end if
    # end write


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_duedates_dr_ids = fields.One2many(
        string='Periodi di slittamento',
        comodel_name='partner.duedates.datarange',
        inverse_name='partner_id',
    )
