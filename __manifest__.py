# Copyright 2020-21 powERP enterprise network <https://www.powerp.it>
#
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Account Banking Common',
    'version': '12.0.3.7.4',
    'category': 'Accounting',
    'summary': 'Common stuff for payment modules',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'OPL-1',
    'depends': [
        'account',
        'account_due_list',
        'account_duedates',
        'account_payment_order',
        'account_payment_method',
    ],
    'data': [
        'views/res_partner_bank_view.xml',
        'views/action_insoluto.xml',
        'wizard/wizard_insoluto.xml',
        'wizard/wizard_payment_order_confirm.xml',
        'wizard/wizard_payment_order_credit.xml',
        'wizard/wizard_account_payment_order_generate.xml',
        'wizard/wizard_account_payment_order_add_move_lines.xml',
        'wizard/wizard_set_payment_method.xml',
        'views/action_payment_confirm.xml',
        'views/account_payment_order.xml',
        'views/action_order_generate.xml',
        'views/action_order_add_move_lines.xml',
        'views/action_duedates_update.xml',
    ],
    'maintainer': 'powERP enterprise network',
    'installable': True,
}
