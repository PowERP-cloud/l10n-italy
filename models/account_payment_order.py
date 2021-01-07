from odoo import models, api, _
from odoo.exceptions import UserError


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'
    
    
    @api.multi
    def unlink(self):
        
        for order in self:
            if order.state != 'cancel':
                raise UserError(
                    f'L\'ordine di pagamento {order.name} non può essere'
                    f'eliminato perché non è nello stato "Annullato"'
                )
            # end if
        # end for
        
        return super(AccountPaymentOrder, self).unlink()
    # end unlink
# end AccountPaymentOrder
