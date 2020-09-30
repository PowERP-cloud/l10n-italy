# -*- coding: utf-8 -*-
#
# Copyright 2017-20 - Axitex Srl
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    'name': 'Invoice due dates',
    'summary': 'Due dates management',
    'version': '12.0.0.1.2',
    'category': 'Accounting',
    'author': 'Axitec Srl',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'account_move_line_due',
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/account_invoice_view.xml',
        'view/account_move_view.xml',
    ],
    'installable': True,
}
