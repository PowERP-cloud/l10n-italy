# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import models, api, fields
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    @api.model
    def get_payment_method_config(self, payment_method_code):
        raise UserError('Non implementato nella classe base')

    def _set_partner_bank_childs(self):
        res = []
        if not self.journal_is_wallet:
            ids = [journal.id for journal in self.journal_wallet_ids]
            domain = [
                ('journal_is_wallet', '=', True),
                ('journal_main_bank_account_id', 'in', ids)]
            res = self.search(domain)

        return res
    # end _set_partner_bank_childs

    def _is_wallet_default(self):
        if self.journal_is_wallet:
            return self.journal_is_wallet
        else:
            return False
        # end if

    # end _is_wallet_default

    @api.depends('bank_wallet_ids')
    def _has_children(self):
        if self.bank_wallet_ids:
            self.has_children = True
        else:
            self.has_children = False
        # end if
    # end _has_children

    bank_is_wallet = fields.Boolean(string="Conto di portafoglio",
                                    default=_is_wallet_default)

    bank_wallet_ids = fields.One2many(
        string='Conti bancari',
        comodel_name='res.partner.bank',
        inverse_name='bank_main_bank_account_id',
        default=_set_partner_bank_childs,
        readonly=True,)

    bank_main_bank_account_id = fields.Many2one(
        string='Conto padre',
        comodel_name='res.partner.bank',
        domain=[('bank_is_wallet', '=', False)],
        default=None
    )

    has_children = fields.Boolean(
        string="Padre",
        compute=_has_children
    )

    journal_is_wallet = fields.Boolean(
        string='Conto di portafoglio',
        related='journal_id.is_wallet'
    )

    journal_wallet_ids = fields.One2many(
        string='Conti di portafoglio',
        related='journal_id.wallet_ids'
    )

    journal_main_bank_account_id = fields.Many2one(
        string='Conto padre',
        related='journal_id.main_bank_account_id'
    )

    display_name = fields.Char(
        string='Name', compute='_compute_display_name',
    )

    @api.onchange('bank_is_wallet')
    def _onchange_bank_is_wallet(self):
        _logger.info('on change su bank_is_wallet')
        if self.journal_id:
            _logger.info('valore is_wallet res_partner_bank |{v}|'.format(v=self.bank_is_wallet))
            journal = self.env['account.journal'].search([('id', '=', self.journal_id.id)])
            journal.write({'is_wallet': self.bank_is_wallet})
            _logger.info('valore is_wallet account_journal {id} |{v}|'.format(v=journal.is_wallet, id=journal.id))
        else:
            _logger.info('valore is_wallet account_journal {id} |{v}|'.format(v=self.journal_id.is_wallet, id=self.journal_id.id))
        # end if
    # _onchange_bank_is_wallet

