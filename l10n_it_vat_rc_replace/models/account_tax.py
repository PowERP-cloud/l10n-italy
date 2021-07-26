# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountTax(models.Model):
    _inherit = 'account.tax'

    @api.multi
    def _default_rc_type(self):
        return self.get_rc_type()
    # end _compute_rc

    rc_type = fields.Selection(
        selection=[
            ('', 'No RC'),
            ('local', 'RC locale'),
            ('self', 'RC con autofattura'),
        ],
        string='Tipo reverse charge',
        default=_default_rc_type,
    )

    rc_sale_tax_id = fields.Many2one(
        comodel_name='account.tax',
        string='Codice iva vendite',
        domain=[('type_tax_use', '=', 'sale')],
    )

    @api.model
    def get_rc_type(self):

        kind_N3 = self.kind_id and self.kind_id.code.startswith('N3')
        kind_N6 = self.kind_id and self.kind_id.code.startswith('N6')

        if kind_N3 and self.kind_id.code != 'N3.5':
            kind = 'self'
        elif kind_N6:
            kind = 'local'
        else:
            kind = ''
        # end if

        return kind
    # end get_rc_type

