# Copyright 2020 PowERP Enterprise Network <https://www.powerp.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
{
    'name': 'Account Banking Common',
    'summary': 'Common stuff for payment modules',
    'version': '12.0.3.4.8',
    'category': 'Accounting',
    'author': 'PowErp Srl',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'account_duedates',
        'account_payment_order',
    ],
    'data': [
        'views/res_partner_bank_view.xml',
        "views/action_insoluto.xml",
        "views/action_test.xml",  # TODO: rimouovere questa action, serve solo per lo sviluppo
        "wizard/wizard_insoluto.xml",
        "views/action_payment_confirm.xml",
        "views/account_payment_order.xml",
        "wizard/wizard_payment_order_confirm.xml",
        "wizard/wizard_payment_order_credit.xml",
    ],
    'installable': True,
}
