#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _get_default_invoice_date(self):
        return (
            fields.Date.today()
            if self._context.get('default_type', 'entry')
            in ('in_invoice', 'in_refund', 'in_receipt')
            else False
        )

    @api.multi
    @api.depends('line_ids')
    def count_line_ids(self):
        for rec in self:
            rec.lines_count = len(rec.line_ids)
        # end for

    # end def

    # Naming of 13.0 differs from account.invoice.date_invoice
    invoice_date = fields.Date(
        string='Data documento',
        readonly=True,
        index=True,
        copy=False,
        states={'draft': [('readonly', False)]},
        default=_get_default_invoice_date,
        help="Keep empty to use the current date",
    )
    # Naming of 13.0 same as account.invoice.type
    # From 14.0 this field is renamed to move_type
    # TODO> rename to move_type
    type = fields.Selection(
        [
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            # ('out_receipt', 'Sales Receipt'),
            # ('in_receipt', 'Purchase Receipt'),
        ],
        readonly=True,
        states={'draft': [('readonly', False)]},
        index=True,
        change_default=True,
        default='entry',
        track_visibility='always',
        required=True,
    )
    fiscal_position_id = fields.Many2one(
        'account.fiscal.position',
        string='Fiscal Position',
        readonly=True,
        states={'draft': [('readonly', False)]},
        domain="[('company_id', '=', company_id)]",
        help="Fiscal positions are used to adapt taxes and accounts for "
        "particular customers or sales orders/invoices. "
        "The default value comes from the customer.",
    )

    lines_count = fields.Integer(compute='count_line_ids')

    payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string='Termine di pagamento',
        oldname='payment_id',
    )

    partner_bank_id = fields.Many2one(
        'res.partner.bank',
        string='Bank Account',
        help=(
            'Bank Account Number to which the invoice will be paid. '
            'A Company bank account if this is a Customer Invoice or '
            'Vendor Credit Note, otherwise a Partner bank account number.'
        ),
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    @api.multi
    def post(self, invoice=False):
        if invoice:
            for move in self:
                for field in ('type',):
                    move[field] = getattr(invoice, field)
                move.move_type = getattr(invoice, 'type')
                move.invoice_date = invoice.date_invoice
                for field in ('payment_term_id',
                              'fiscal_position_id',
                              'partner_bank_id'):
                    move[field] = getattr(invoice, field)
        return super().post(invoice=invoice)
