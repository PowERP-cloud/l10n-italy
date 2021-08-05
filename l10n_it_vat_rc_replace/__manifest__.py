# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    'name': 'ITA - Inversione contabile',
    'version': '12.0.1.2.7_22',
    'category': 'Localization/Italy',
    'summary': 'Inversione contabile',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_cancel',
        'l10n_it_account_tax_kind',
        'account_move_line_type',
        'l10n_it_fatturapa_in',
        'l10n_it_fatturapa_out',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/rc_type.xml',
        'views/account_invoice_view.xml',
        'views/account_fiscal_position_view.xml',
        'views/account_rc_type_view.xml',
        'views/account_tax_view.xml',
        'security/reverse_charge_security.xml',
    ],
    'maintainer': 'powERP enterprise network',
    'installable': True,
}
