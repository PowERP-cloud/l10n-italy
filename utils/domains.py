from . import misc


BANK_EXPENSES_ACCOUNT_EXTERNAL_ID = 'account.data_account_type_expenses'


transfer_journal = [
    ('type', 'not in', ['sale', 'sale_refund', 'purchase', 'purchase_refund'])
]
sezionale = transfer_journal

transfer_account = [
    ('user_type_id.type', '=', 'receivable')
]
conto_effetti_attivi = transfer_account

banca_conto_effetti = [
    ('user_type_id.type', 'in', ['bank', 'receivable'])
]


def get_bank_expenses_account(env):
    acct_type_id = misc.external_id_to_id(
        env, BANK_EXPENSES_ACCOUNT_EXTERNAL_ID
    )
    return [('user_type_id', '=', acct_type_id)]
# end get_bank_expenses_account


get_expenses_account = get_bank_expenses_account
