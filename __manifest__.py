# Copyright 2020 PowERP Enterprise Network <https://www.powerp.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
{
    'name': 'Account Banking Common',
    'summary': 'Common stuff for payment modules',
    'version': '12.0.3.5.14',
    'category': 'Accounting',
    'author': 'powERP, Didotech srl, SHS-AV srl',
    'website': 'www.powerp.it',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'account_duedates',
        'account_payment_order',
    ],
    'data': [
        'views/res_partner_bank_view.xml',
        "views/action_insoluto.xml",
        "wizard/wizard_insoluto.xml",
        "views/action_payment_confirm.xml",
        "views/account_payment_order.xml",
        "wizard/wizard_payment_order_confirm.xml",
        "wizard/wizard_payment_order_credit.xml",
    ],
    'installable': True,
    'maintainer': 'powERP enterprise network'
}
