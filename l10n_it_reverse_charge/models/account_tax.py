# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountTax(models.Model):
    _inherit = 'account.tax'

    @api.multi
    def _compute_rc(self):
        for tax in self:
            tax.rc_type = tax.get_rc_type()
        # end for

    # end _compute_rc

    # rc_type = fields.Char('Tipo RC', compute='_compute_rc')
    rc_type = fields.Selection(
        selection=[
            ('', 'No RC'),
            ('local', 'RC locale'),
            ('self', 'RC con autofattura'),
        ],
        string='Tipo reverse charge',
        compute='_compute_rc',
    )

    rc_sale_tax_id = fields.Many2one(
        comodel_name='account.tax',
        string='Codice iva vendite',
        domain=[('type_tax_use', '=', 'sale')],
    )

    @api.model
    def get_rc_type(self):

        if self.kind_id and self.kind_id.code.startswith('N3') and \
            self.kind_id.code != 'N3.5':
            kind = 'self'
        elif self.kind_id and self.kind_id.code.startswith('N6'):
            kind = 'local'
        else:
            kind = ''
        # end if

        return kind
    # end get_rc_type

