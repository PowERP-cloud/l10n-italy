import typing

from odoo.exceptions import UserError


def same_payment_method(account_move_lines):
    '''Ensures all lines have the same payment method'''
    
    pay_code = None
    
    for line in account_move_lines:
        
        line_pay_code = line.payment_method.code
        
        if pay_code is None:
            pay_code = line_pay_code
            
        elif line_pay_code != pay_code:
            raise UserError(
                'Le scadenze selezionate devono avere '
                'tutte lo stesso metodo di pagamento'
            )
        
        else:
            pass
        
        # end if
        
    # end for
    
# end same_payment_method


def allowed_payment_method(account_move_lines, payment_method_codes: typing.List):
    
    for line in account_move_lines:
        
        if line.payment_method.code not in payment_method_codes:
            raise UserError(
                'La funzione è supportata solo '
                'per i seguenti metodi di pagamento:'
                ' ' + ', '.join(payment_method_codes)
            )
        # end if
        
    # end for
    
# end allowed_payment_method


def assigned_to_payment_order(account_move_lines, assigned: bool):
    
    for line in account_move_lines:

        if assigned and not line.in_order:
            raise UserError(
                'Le scadenze selezionate devono essere '
                'assegnate ad un ordine di pagamento'
            )
        elif not assigned and line.in_order:
            raise UserError(
                'Le scadenze selezionate non possono essere '
                'già assegnate ad un ordine di pagamento'
            )
        else:
            pass
        # end if
        
    # end for
    
# end assigned_to_payment_order


def allowed_payment_order_status(account_move_lines, payment_order_status: typing.List):
    for line in account_move_lines:

        if line.state not in payment_order_status:
            raise UserError(
                'Per poter procedere con l\'operazione l\'ordine '
                'di pagamento di ciascuna scadenza selezionata deve '
                'essere nello stato "Documento Caricato"'
            )
        # end if
        
    # end for
    
# end assigned_to_payment_order
