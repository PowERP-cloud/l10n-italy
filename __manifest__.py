# Copyright 2020 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
{
    'name': 'Due dates',
    'summary': 'Due dates management',
    'version': '12.0.0.1.26',
    'category': 'Accounting',
    'author': 'Axitec Srl',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'account_due_list',
        'account_move_plus',
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/account_invoice_view.xml',
        'view/account_move_view.xml',
        'view/account_move_line_view.xml',
        'view/account_due_list_view.xml',
    ],
    'installable': True,
    # 'post_init_hook': 'post_init_hook',
}
