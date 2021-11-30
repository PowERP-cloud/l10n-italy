# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Account Payment Method',
    'version': '12.0.0.2.6',
    'category': 'Generic Modules/Accounting',
    'summary': 'Extend payment method model',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'account_payment_mode',
    ],
    'data': [
        'views/payment_method_view.xml',
        'data/payment_method.xml',
    ],
    'maintainer': 'powERP enterprise network',
    'installable': True,
}
