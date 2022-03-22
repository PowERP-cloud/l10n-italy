# Copyright 2016 Davide Corio
# Copyright 2017 Alex Comba - Agile Business Group
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2017 Marco Calcagni - Dinamiche Aziendali srl
# Copyright 2021 Antonio M. Vigliotti - SHS-Av srl
# Copyright 2021 powERP enterprise network <https://www.librerp.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#

from odoo import fields, models


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    # rc_type_id = fields.Many2one('account.rc.type', 'RC Type')

    rc_type = fields.Selection(
        selection=[
            ('', 'No RC'),
            ('local', 'RC locale'),
            ('self', 'RC con autofattura'),
        ],
        string='Reverse charge',
        default='',
    )

    partner_type = fields.Selection(
        selection=[
            ('supplier', 'Fornitore'),
            ('other', 'Azienda')
        ],
        string='Tipo di Partner',
        default='',
    )

    self_journal_id = fields.Many2one(
        'account.journal',
        string='Registro per autofattura',
        domain=[('type', '=', 'sale')],
        default='',
    )

    rc_fiscal_document_type_id = fields.Many2one(
        'fiscal.document.type',
        string="Self Invoice Fiscal Document Type",
        )
