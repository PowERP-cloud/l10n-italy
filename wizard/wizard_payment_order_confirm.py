#
# Copyright 2017-20 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Copyright 2020 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import logging
from odoo import models, api, fields
# from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WizardPaymentOrderConfirm(models.TransientModel):
    _name = 'wizard.payment.order.confirm'
    _description = 'Create confirm payment wizard from due dates tree view'

    account_expense = fields.Many2one(
        'account.account',
        string='Conto spese',
        domain=[(
            'internal_group', '=', 'expense')]
    )

    amount_expense = fields.Float(string='Importo', )

    @api.multi
    def confirm(self):

        active_ids = self._context.get('active_ids')

        # Debug - begin
        print('Active ids:', active_ids)
        # Debug - end

        # payment_mode_id = self.env['account.payment.mode'].search([(
        #     'payment_method_code', '=', 'invoice_financing')])

        if len(active_ids) > 0:
            pass
            # lines = self.env['account.move.line'].browse(active_ids)

            # Check for errors

            # per ogni riga verificare:
            # - tipo documento f nc
            # - la banca
            # - get_payment_method_config


            # Creazione registrazione contabile
            # payment_order = self.env['account.payment.order'].create({
            #     'payment_mode_id': payment_mode_id.id,
            #     'journal_id': account_config['sezionale'].id,
            #     'description': '',
            # })

            # Aggiunta linee a distinta
            # TODO
            # lines.create_payment_line_from_move_line(payment_order)

            # Apertura ordine di pagamento
            # return {
            #     'type': 'ir.actions.act_window',
            #     'res_model': 'account.payment.order',
            #     'res_id': payment_order.id,
            #     'view_mode': 'form',
            #     'views': [(False, 'form')],
            #     'target': 'current',
            # }
        # end if
    # end confirm()

# end AccountPaymentGenerate
