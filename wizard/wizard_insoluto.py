import logging

from odoo import models, api, fields

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
    
    @api.multi
    def registra_insoluto(self):
        print('registra_insoluto()')
    # end registra_insoluto
    
# end WizardInsoluto
