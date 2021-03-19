import logging
from odoo import api, SUPERUSER_ID
from odoo.exceptions import UserError


logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """
    The objective of this hook is to detect the installation
    of the module 'account_payment_term_extension' on an
    existing Odoo instance.
    """

    env = api.Environment(cr, SUPERUSER_ID, {})
    installed_module = env['ir.module.module'].search([
        ('name', '=', 'account_payment_term_extension')
    ])
    if installed_module and installed_module.state == 'installed':
        raise UserError('Questo modulo non è installabile poichè è '
                        'presente un\'altra versione simile '
                        '(account_payment_term_extension).')
