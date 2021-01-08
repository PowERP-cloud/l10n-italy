import logging

from odoo import models, api, fields
from odoo.exceptions import UserError

from ..utils import domains

_logger = logging.getLogger(__name__)


class WizardInsoluto(models.TransientModel):
    
    _name = 'wizard.account.banking.common.insoluto'
    _description = 'Gestione insoluti'

    expenses_account = fields.Many2one(
        'account.account',
        string='Conto Spese',
        domain=domains.expenses_account,
    )
    
    expenses_amount = fields.Float(string='Importo spese')
    
    charge_client = fields.Boolean(
        string='Addebito spese a cliente',
        default=False,
    )
    
    @api.multi
    def registra_insoluto(self):
        '''Create on new account.move for each line of insoluto'''
        ids = self._context['active_ids']
        model = self.env['account.move.line']
        recordset = model.browse(ids)
        recordset.registra_insoluto()
    # end registra_insoluto
    
# end WizardInsoluto
