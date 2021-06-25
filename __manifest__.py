# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Due dates',
    'version': '12.0.4.8.11',
    'category': 'Accounting',
    'summary': 'Due dates management',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'OPL-1',
    'depends': [
        'account',
        'base',
        'account_due_list',
        'account_move_plus',
        'account_payment_order',
        'account_invoice_13_more',
        'account_move_line_type',
        'date_range_plus',
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
    'maintainer': 'powERP enterprise network',
    'installable': True,
    'post_init_hook': 'post_init_hook',
}
