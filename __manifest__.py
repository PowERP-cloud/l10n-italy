# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Account Move Plus',
    'version': '12.0.0.2.5',
    'category': 'Accounting',
    'summary': 'Account move extension for Italian Localization',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'base',
        'date_range_plus',
        'account_fiscal_year',
    ],
    'data': ['views/account_move_view.xml'],
    'installable': True,
}
