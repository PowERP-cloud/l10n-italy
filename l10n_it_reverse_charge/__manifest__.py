# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'ITA - Inversione contabile',
    'version': '12.0.1.2.8',
    'category': 'Localization/Italy',
    'summary': 'Inversione contabile',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    # 'license': 'OPL-1',  # Non può essere OPL-1 perchè dipende da l10n_it_account_tax_kind che è AGPL-3
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_cancel',
        'l10n_it_account_tax_kind',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/rc_type.xml',
        'views/account_invoice_view.xml',
        'views/account_fiscal_position_view.xml',
        'views/account_rc_type_view.xml',
        'security/reverse_charge_security.xml',
    ],
    'maintainer': 'powERP enterprise network',
    'installable': True,
    'pre_init_hook': 'pre_init_hook',
}
