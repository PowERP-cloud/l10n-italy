{
    'name': 'Intrastat esteso',
    'version': '12.0.1.2.5',
    'category': 'Account',
    'summary': 'Riclassificazione merci e servizi per dichiarazioni Intrastat',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'l10n_it_ddt',
        'l10n_it_intrastat',
        'l10n_it_costs_allocation',
    ],
    'data': [
        'views/account.xml',
        'views/res_config_settings_views.xml',
        'report/report_invoice.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
