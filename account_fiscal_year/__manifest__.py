# Copyright 2016 Camptocamp SA
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    'name': 'Account Fiscal Year',
    'version': '12.0.1.1.1',
    'category': 'Accounting',
    'summary': 'Create a menu for Account Fiscal Year',
    'author': 'Odoo Community Association (OCA) and other partners',
    'website': 'https://odoo-community.org',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'date_range_plus',
    ],
    'data': [
        'data/date_range_type.xml',
        'views/account_views.xml',
    ],
    'installable': True,
    'maintainers': ['eLBati'],
    'application': False,
}
