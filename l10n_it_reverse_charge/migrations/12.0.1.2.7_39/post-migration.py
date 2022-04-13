# Copyright 2021-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2021-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021-22 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import api, SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)


def set_rc_purchase_tax(cr):
    """Link sale RC tax with its parent purchase RC tax

    Args:
        cr (obj): sql cursor

    Returns:
        None
    """
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        tax_model = env['account.tax']
        for tax in tax_model.search([]):
            if tax.rc_sale_tax_id:
                tax.rc_sale_tax_id.rc_purchase_tax_id = tax.id


def migrate(cr, version):
    if not version:
        return

    set_rc_purchase_tax(cr)

    _logger.info("set_rc_purchase_tax migration executed successfully ...")
