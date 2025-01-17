# Copyright 2021-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2021-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021-22 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
import logging

from odoo import SUPERUSER_ID, api
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """
    The objective of this hook is to detect the installation
    of the module 'l10n_it_reverse_charge' on an
    existing Odoo instance.
    """

    env = api.Environment(cr, SUPERUSER_ID, {})

    # incompatibility check
    parameter = env["ir.config_parameter"].search(
        [("key", "=", "disable_oca_incompatibility")]
    )

    if not parameter or not eval(parameter.value):
        installed_module = env["ir.module.module"].search(
            [("name", "=", "l10n_it_reverse_charge")]
        )
        if (
            installed_module
            and installed_module.maintainer.lower() != "librerp enterprise network"
        ):
            raise UserError(
                "Questo modulo non è installabile poichè è "
                "presente un'altra versione di "
                "(l10n_it_reverse_charge)."
            )
        # end if
    # end if
