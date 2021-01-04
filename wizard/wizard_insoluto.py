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
    
    @api.multi
    def registra_insoluto(self):
        '''Create on new account.move for each line of insoluto'''
        
        recordset = self.env['account.move.line'].browse(
            self._context['active_ids']
        )
        
        for r in recordset:
            
            # - - - - - - - - - - - - - - - - -
            # Retrieve the payment order data
            # - - - - - - - - - - - - - - - - -
            
            pol = r.payment_order_lines[0]  # Payment order line
            po = pol.order_id  # Payment order
            
            pol_partner = pol.partner_id  # Partner for this duedate
            po_journal = po.journal_id  # Journal selected in the po
            bank = po.company_partner_bank_id  # Bank selected in the po

            # The payment method of the payment order
            pm = po.payment_method_id
            
            # - - - - - - - - - - - - - - -
            # Payment method configuration
            # - - - - - - - - - - - - - - -
            
            # Get the account.journal to be used fo the new account.move
            mv_journal = bank.get_payment_method_config(pm.code)['sezionale']
            if not mv_journal:
                raise UserError(
                    f'"Sezionale" non configurato per c/c {bank.acc_number}'
                )
            # end if
            
            # account.account -> Bank
            acct_acct_bank = po_journal.default_credit_account_id
            if not acct_acct_bank:
                raise UserError(
                    f'Conto "avere" non configurato per non configurato per '
                    f'sezionale di banca '
                    f'{po_journal.display_name} ({po_journal.code})'
                )
            # end if
            
            # account.account -> Partner
            acct_acct_part = r.account_id
            
            # account.account -> Expenses
            acct_acct_expe = self.expenses_account
            
            # - - - - - - - - - - - - - -
            # New account.move creation
            # - - - - - - - - - - - - - -
            
            # 1 - Move lines
            move_lines = [
                (0, 0, {
                    'account_id': acct_acct_part.id,
                    'partner_id': pol_partner.id,
                    'credit': 0, 'debit': r.debit
                }),
                (0, 0, {
                    'account_id': acct_acct_bank.id,
                    'credit': r.debit + self.expenses_amount, 'debit': 0
                }),
            ]
            
            if acct_acct_expe:
                move_lines.append(
                    (0, 0, {
                        'account_id': acct_acct_expe.id,
                        'credit': 0, 'debit': self.expenses_amount
                    }),
                )
            # end if
            
            # 2 - New account.move as draft
            # account_move = self.env['account.move'].create({
            self.env['account.move'].create({
                'type': 'entry',
                'date': fields.Date.today(),
                'journal_id': mv_journal.id,
                'state': 'draft',
                'ref': 'Insoluto',
                'line_ids': move_lines,
            })
            
        # end for
        
    # end registra_insoluto
    
# end WizardInsoluto
