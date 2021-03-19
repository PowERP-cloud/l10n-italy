# Copyright 2020 PowERP Enterprise Network <https://www.powerp.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
{
    'name': 'Account Banking Common',
    'summary': 'Common stuff for payment modules',
    'version': '12.0.3.7.3',
    'category': 'Accounting',
    'author': 'powERP, Didotech srl, SHS-AV srl',
    'website': 'www.powerp.it',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'account_due_list',
        'account_duedates',
        'account_payment_order',
        'account_payment_method',
    ],
    'data': [
        'views/res_partner_bank_view.xml',
        "views/action_insoluto.xml",
        "wizard/wizard_insoluto.xml",
        "wizard/wizard_payment_order_confirm.xml",
        "wizard/wizard_payment_order_credit.xml",
        "wizard/wizard_account_payment_order_generate.xml",
        "wizard/wizard_account_payment_order_add_move_lines.xml",
        "wizard/wizard_set_payment_method.xml",
        "views/action_payment_confirm.xml",
        "views/account_payment_order.xml",
        # "views/account_due_list_view.xml",
        "views/action_order_generate.xml",
        "views/action_order_add_move_lines.xml",
        "views/action_duedates_update.xml",
    ],
    'installable': True,
    'maintainer': 'powERP enterprise network'
}
