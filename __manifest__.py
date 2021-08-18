# Copyright 2013-16 Camptocamp SA (Yannick Vaucher)
# Copyright 2015-16 Akretion
# (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Payment Term Extension Plus',
    'version': '12.0.0.1.8',
    'category': 'Accounting & Finance',
    'summary': 'Adds rounding, months, weeks and multiple payment days properties on payment term lines',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_payment_method',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard_duedates_simulator.xml',
        'views/account_payment_term.xml',
    ],
    'maintainer': 'powERP enterprise network',
    'installable': True,
    'pre_init_hook': 'pre_init_hook',
}
