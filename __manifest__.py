#
# Copyright (c) 2020
#
{
    'name': 'Account Move Plus',
    'summary': 'Account move extension for Italian Localization',
    'version': '12.0.0.1.2',
    'category': 'Accounting',
    'author': 'Didotech srl',
    'website': 'https://www.didotech.com/',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'base',
        'date_range',
        'account_fiscal_year',
        'account_invoice_entry_dates',
    ],
    'data': [
        'views/account_move_view.xml',
    ],
    'installable': True,
}
