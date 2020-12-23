# Copyright 2013-2016 Camptocamp SA (Yannick Vaucher)
# Copyright 2015-2016 Akretion
# (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Payment Term Extension Plus',
    'version': '12.0.0.1.7',
    'category': 'Accounting & Finance',
    'summary': 'Adds rounding, months, weeks and multiple payment days '
               'properties on payment term lines',
    'author': 'Odoo Community Association (OCA), '
              'Didotech srl',
    'maintainer': 'Didotech srl',
    'website': 'http://didotech.com/',
    'license': 'LGPL-3',
    'depends': ['account', 'account_payment_method'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard_duedates_simulator.xml',
        'views/account_payment_term.xml',
    ],
    'installable': True,
    'pre_init_hook': 'pre_init_hook',
}
