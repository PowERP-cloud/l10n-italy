# Copyright 2020 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import logging
# from odoo import api, SUPERUSER_ID
# from odoo.exceptions import UserError


logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """
    The objective of this hook is to update account move line new field
    with the correct value.
    """

    # env = api.Environment(cr, SUPERUSER_ID, {})

    query = """UPDATE account_move_line 
    set due_dc = 'C' where user_type_id in
    (select id from account_account_type
    where type = 'receivable')"""
    cr.execute(query)

    query = """UPDATE account_move_line 
    set due_dc = 'D' where user_type_id in
    (select id from account_account_type
    where type = 'payable')"""
    cr.execute(query)

# end post_init_hook
