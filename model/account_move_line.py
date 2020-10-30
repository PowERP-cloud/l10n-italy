#
# Copyright 2020 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#


import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    payment_method = fields.Many2one('account.payment.method',
                                     string="Metodo di pagamento")

    calculate_field = fields.Char(string='Domain test', compute='_domain_test')

    is_duedate = fields.Boolean(
        string='Riga di scadenza',
        compute='_compute_is_dudate'
    )

    duedate_line_id = fields.Many2one(
        'account.duedate_plus.line',
        string='Riferimento riga scadenza',
        indexed=True,
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ONCHANGE METHODS

    @api.onchange('account_id')
    def onchange_account_id(self):

        domain = []

        if self.account_id:
            account_type = self.env['account.account.type'].search(
                [('id', '=', self.account_id.user_type_id.id)])
            if account_type:
                if account_type.type == 'payable':
                    # self.due_dc = 'D'
                    domain = ['|', ('debit_credit', '=', 'debit'),
                              ('debit_credit', '=', False)]
                elif account_type.type == 'receivable':
                    # self.due_dc = 'C'
                    domain = ['|', ('debit_credit', '=', 'credit'),
                              ('debit_credit', '=', False)]
                # else:
                #     self.due_dc = ''
                # end if
            # end if
        # end if

        return {'domain': {'payment_method': domain}}

    # end onchange_account_id

    # ONCHANGE METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @api.model
    def _compute_is_dudate(self):
        for line in self:

            not_vat_line = (not line.tax_ids) and (not line.tax_line_id)
            credit_or_debit = line.account_id.user_type_id.type in (
                'payable', 'receivable'
            )

            line.is_duedate = not_vat_line and credit_or_debit
        # end for
    # end _compute_is_dudate

    def _domain_test(self):
        for rec in self:
            if rec.account_id:
                account_type = self.env['account.account.type'].search(
                    [('id', '=', rec.account_id.user_type_id.id)])
                if account_type:
                    if account_type.type == 'payable':
                        rec.calculate_field = 'debit'
                    elif account_type.type == 'receivable':
                        rec.calculate_field = 'credit'


    @api.model
    def create(self, values):
        print('account.move.line - create - begin')
        print('\t', values)
        res = super().create(values)
        print('account.move.line - create - end')
        return res
    # end create

    @api.multi
    def write(self, values):
        print('account.move.line - write - begin')
        print('\t', values)

        print('account.move.line - write - super() - begin')
        result = super().write(values)
        print('account.move.line - write - super() - end')

        if not self.env.context.get('RecStop'):
            if 'date_maturity' in values:
                for move in self:
                    print('account.move.line - write - move({}).update_date_maturity() - begin'.format(move.id))
                    move.with_context(
                        RecStop=True
                    ).update_date_maturity()
                    print('account.move.line - write - move({}).update_date_maturity() - end'.format(move.id))
                # end for
            # end if

            if 'payment_method' in values:
                for move in self:
                    print('account.move.line - write - move({}).update_payment_method() - begin'.format(move.id))
                    move.with_context(
                        RecStop=True
                    ).update_payment_method()
                    print('account.move.line - write - move({}).update_payment_method() - end'.format(move.id))
                # end for
            # end if
        # end if

        print('account.move.line - write - end')
        return result
    # end write

    # Update the associated duedate_line
    @api.model
    def update_date_maturity(self):
        if self.duedate_line_id:
            self.duedate_line_id.due_date = self.date_maturity
    # end _update_date_maturity

    @api.model
    def update_payment_method(self):
        if self.duedate_line_id:
            self.duedate_line_id.payment_method_id = self.payment_method
    # end _update_payment_method
# end AccountMoveLine
