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
    '''Ensures the selected lines have a supported payment method'''
    
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
    '''
    Check if the selected lines are assigned to a payment order or not.
    If the "assigned" parameters is:
    
      - True the method requires that all lines have been assigned to a
        payment order, raises an exception otherwise
    
      - False the method requires that all lines have NOT been assigned to a
        payment order, raises an exception otherwise
    '''
    
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
    '''
    Ensures that all the payment orders referenced by the lines are in one of
    the valid statuses listed in the payment_order_status parameter
    '''
    
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


def except_payment_order_status(account_move_lines,
                                payment_order_status: typing.List):
    '''
    Ensures that all the payment orders referenced by the lines are not in
    one of the valid statuses listed in the payment_order_status parameter
    '''

    for line in account_move_lines:

        if line.state in payment_order_status:
            raise UserError(
                'Per poter procedere con l\'operazione l\'ordine '
                'di pagamento di ciascuna scadenza selezionata non deve '
                'essere nello stato "Documento Caricato"'
            )
        # end if

    # end for

# end except_payment_order_status

