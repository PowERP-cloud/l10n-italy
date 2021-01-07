# Copyright 2020 PowERP Enterprise Network <https://www.powerp.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
{
    'name': 'Account Banking Common',
    'summary': 'Common stuff for payment modules',
    'version': '12.0.2.4.6',
    'category': 'Accounting',
    'author': 'PowErp Srl',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'account_duedates',
    ],
    'data': [
        'views/res_partner_bank_view.xml',
        "views/action_insoluto.xml",
        "wizard/wizard_insoluto.xml",
        "views/action_payment_confirm.xml",
        "wizard/wizard_payment_order_confirm.xml",
    ],
    'installable': True,
}
