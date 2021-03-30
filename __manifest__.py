# Copyright 2020 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
{
    'name': 'Due dates',
    'summary': 'Due dates management',
    'version': '12.0.3.2.1',
    'category': 'Accounting',
    'author': 'powERP, Didotech srl, SHS-AV srl',
    'website': 'www.powerp.it',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'account_due_list',
        'account_move_plus',
        'account_payment_order',
        'account_invoice_13_more',
        'account_move_line_type',
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/account_invoice_view.xml',
        'view/account_move_view.xml',
        'view/account_move_line_view.xml',
        'view/account_due_list_view.xml',
    ],
    'installable': True,
    'maintainer': 'powERP enterprise network'
    # 'post_init_hook': 'post_init_hook',
}
