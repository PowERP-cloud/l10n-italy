# Copyright 2020 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
{
    'name': 'Due dates',
    'summary': 'Due dates management',
    'version': '12.0.3.3.8',
    'category': 'Accounting',
    'author': 'powERP, Didotech srl, SHS-AV srl',
    'website': 'www.powerp.it',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'base',
        'account_due_list',
        'account_move_plus',
        'account_payment_order',
        'account_invoice_13_more',
        'account_move_line_type',
        'date_range',
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/account_invoice_view.xml',
        'view/account_move_view.xml',
        'view/account_move_line_view.xml',
        'view/account_due_list_view.xml',
        'view/partner_view.xml',
        'data/update_year_cron.xml',
        'data/date_range_type.xml',
    ],
    'installable': True,
    'maintainer': 'powERP enterprise network',
    'post_init_hook': 'post_init_hook',
}
