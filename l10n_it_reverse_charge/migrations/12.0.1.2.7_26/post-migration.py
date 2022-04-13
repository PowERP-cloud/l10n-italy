# Copyright 2021-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2021-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021-22 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
import logging
_logger = logging.getLogger(__name__)


def _update_account_move(cr):

    cr.execute("SELECT move_id, partner_id FROM account_move_line WHERE "
               "move_id in (SELECT id FROM public.account_move WHERE "
               "type = 'in_invoice' AND partner_id IS NULL AND "
               "name like 'ACQ%' AND state = 'posted') "
               "AND user_type_id = 2 GROUP BY move_id, partner_id")

    records = cr.fetchall()
    for record in records:
        sql = "update account_move set partner_id = {partner} where " \
              "id = {move}".format(partner=record[1], move=record[0])
        _logger.info(sql)
        cr.execute(sql)


def migrate(cr, version):
    if not version:
        _logger.warning("Does not exist any previous version for this module. "
                        "Skipping the migration...")

        return

    _update_account_move(cr)

    _logger.info("Migration executed successfully. Exiting...")
