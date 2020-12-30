sezionale = [
    ('type', 'not in', ['sale', 'sale_refund', 'purchase', 'purchase_refund'])
]

conto_effetti_attivi = [
        ('nature', 'in', ['A', 'P']),
        ('user_type_id.name', 'in', [
            'Receivable',
            'Bank and Cash',
            'Current Assets',
            'Credito',
            'Banca e cassa',
            'Attività correnti']), ]

banca_conto_effetti = [('nature', 'in', ['A', 'P'])]

expenses_account = [('internal_group', '=', 'expense')]
