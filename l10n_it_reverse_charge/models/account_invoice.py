# Copyright 2016 Davide Corio
# Copyright 2017 Alex Comba - Agile Business Group
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2017 Marco Calcagni - Dinamiche Aziendali srl
# Copyright 2021 Antonio M. Vigliotti - SHS-Av srl
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#

from odoo import api, fields, models
from odoo.exceptions import Warning as UserError
from odoo.tools.translate import _
import odoo.addons.decimal_precision as dp
from odoo.tools import float_compare


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.depends("invoice_id")
    def compute_rc_type(self):
        for line in self:
            if line.invoice_id.fiscal_position_id.rc_type:
                line.line_rc_type = True
            else:
                line.line_rc_type = False
            # end if

        # end for
    # end compute_rc_type

    @api.multi
    def _set_rc_flag(self, invoice):
        self.ensure_one()
        if invoice.type in ['in_invoice', 'in_refund']:
            for tax in self.invoice_line_tax_ids:
                if tax.rc_type:
                    self.rc = True
                else:
                    self.rc = False
                # end if
            # end for
        # end fi
    # end _set_rc_flag

    @api.onchange('invoice_line_tax_ids')
    def onchange_invoice_line_tax_id(self):
        res = dict()
        invoice_rc_type = self.invoice_id.fiscal_position_id.rc_type
        if self.invoice_id.type in ['in_invoice', 'in_refund']:
            for tax in self.invoice_line_tax_ids:

                is_rc_self = invoice_rc_type == 'self'
                rc_mismatch = tax.rc_type != invoice_rc_type

                if is_rc_self and rc_mismatch:
                    raise UserError(
                        'Natura esenzione errata per la tassa impostata.'
                    )
                # end if
            # end for
        # end if

        if not res:
            self._set_rc_flag(self.invoice_id)
        # end if

        return res

    rc = fields.Boolean("RC")

    line_rc_type = fields.Boolean("Has RC", compute='compute_rc_type')
    # line_rc_type = fields.Selection("Has RC",
    #                                 related='invoice_id.fiscal_position_id.rc_type')

    def _set_additional_fields(self, invoice):
        self._set_rc_flag(invoice)
        return super(AccountInvoiceLine, self)._set_additional_fields(invoice)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.depends('invoice_line_ids')
    def _compute_amount_rc(self):
        for inv in self:
            inv.amount_rc = inv.compute_rc_amount_tax()
        # end for
    # end _compute_amount_rc

    @api.depends('fiscal_position_id')
    def _compute_rc_type(self):
        for inv in self:
            inv.rc_type = inv.fiscal_position_id.rc_type
        # end for
    # end _compute_rc_type

    @api.depends('amount_total', 'amount_rc')
    def _compute_net_pay(self):
        res = super()._compute_net_pay()
        for inv in self:
            if inv.fiscal_position_id.rc_type:
                inv.amount_net_pay = inv.amount_total - inv.amount_rc
        # end for
    # end _compute_net_pay

    rc_self_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='RC Self Invoice',
        copy=False, readonly=True)
    rc_purchase_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='RC Purchase Invoice', copy=False, readonly=True)
    rc_self_purchase_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='RC Self Purchase Invoice', copy=False, readonly=True)

    amount_rc = fields.Float(
        string='Iva RC',
        digits=dp.get_precision('Account'),
        store=True,
        readonly=True,
        compute='_compute_amount_rc')

    rc_type = fields.Char(
        string='RC Type',
        compute='_compute_rc_type',
    )

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.fiscal_position_id and res.fiscal_position_id.rc_type:
            for line in res.invoice_line_ids:
                line._set_rc_flag(res)
        return res

    @api.multi
    def write(self, values):

        result = super().write(values)

        stop_recursion = self.env.context.get('StopRecursion', False)

        if not stop_recursion:
            # Enable stop recursion
            self = self.with_context(StopRecursion=True)

            for inv in self:
                if inv.rc_type:
                    inv.amount_rc = inv.compute_rc_amount_tax()
            # end for
        # end if
        return result
    # end write

    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_ids(self):
        super()._onchange_invoice_line_ids()
        for line in self.invoice_line_ids:
            line._set_rc_flag(self)

    @api.onchange('fiscal_position_id')
    def onchange_rc_fiscal_position_id(self):
        for line in self.invoice_line_ids:
            line._set_rc_flag(self)

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
        # In some cases (like creating the invoice from PO),
        # fiscal position's onchange is triggered
        # before than being changed by this method.
        self.onchange_rc_fiscal_position_id()
        return res

    # tenere
    def _compute_amount(self):
        super()._compute_amount()
        for inv in self:
            if inv.rc_type:
                inv.amount_total = inv.amount_untaxed + inv.amount_tax
                if inv.rc_type == 'self':
                    inv.amount_tax = 0
                elif inv.rc_type == 'local':
                    inv.amount_tax -= inv.amount_rc
        # end if
    # end _compute_amount

    # tenere
    def rc_inv_line_vals(self, line):
        return {
            'product_id': line.product_id.id,
            'name': line.name,
            'uom_id': line.product_id.uom_id.id,
            'price_unit': line.price_unit,
            'quantity': line.quantity,
            'discount': line.discount,
            }

    # tenere
    def rc_inv_vals(self, partner, account, journal_id, lines, currency):
        if self.type == 'in_invoice':
            type = 'out_invoice'
        else:
            type = 'out_refund'

        comment = _(
            "Reverse charge self invoice.\n"
            "Supplier: %s\n"
            "Reference: %s\n"
            "Date: %s\n"
            "Internal reference: %s") % (
            self.partner_id.display_name, self.reference or '', self.date,
            self.number
        )
        return {
            'partner_id': partner.id,
            'type': type,
            'account_id': account.id,
            'journal_id': journal_id.id,
            'invoice_line_ids': lines,
            'date_invoice': self.date,
            'date': self.date,
            'origin': self.number,
            'rc_purchase_invoice_id': self.id,
            'name': 'Reverse charge self invoice',
            'currency_id': currency.id,
            'fiscal_position_id': False,
            'payment_term_id': False,
            'comment': comment,
            }

    def get_inv_line_to_reconcile(self):
        for inv_line in self.move_id.line_ids:
            if (self.type == 'in_invoice') and inv_line.credit:
                return inv_line
            elif (self.type == 'in_refund') and inv_line.debit:
                return inv_line
        return False

    def get_rc_inv_line_to_reconcile(self, invoice):
        for inv_line in invoice.move_id.line_ids:
            if (invoice.type == 'out_invoice') and inv_line.debit:
                return inv_line
            elif (invoice.type == 'out_refund') and inv_line.credit:
                return inv_line
        return False

    def rc_payment_vals(self, rc_type):
        return {
            'journal_id': rc_type.payment_journal_id.id,
            # 'period_id': self.period_id.id,
            'date': self.date,
            }

    # tenere
    def compute_rc_amount_tax(self):
        rc_amount_tax = 0.0
        round_curr = self.currency_id.round
        rc_lines = self.invoice_line_ids.filtered(lambda l: l.rc)
        for rc_line in rc_lines:
            price_unit = \
                rc_line.price_unit * (1 - (rc_line.discount or 0.0) / 100.0)
            taxes = rc_line.invoice_line_tax_ids.compute_all(
                price_unit,
                self.currency_id,
                rc_line.quantity,
                product=rc_line.product_id,
                partner=rc_line.partner_id)['taxes']
            rc_amount_tax += sum([tax['amount'] for tax in taxes])

        # convert the amount to main company currency, as
        # compute_rc_amount_tax is used for debit/credit fields
        invoice_currency = self.currency_id.with_context(
            date=self.date_invoice)
        main_currency = self.company_currency_id.with_context(
            date=self.date_invoice)
        if invoice_currency != main_currency:
            round_curr = main_currency.round
            rc_amount_tax = invoice_currency.compute(
                rc_amount_tax, main_currency)

        return round_curr(rc_amount_tax)

    def rc_credit_line_vals(self, journal):
        credit = debit = 0.0
        amount_rc_tax = self.compute_rc_amount_tax()

        if self.type == 'in_invoice':
            credit = amount_rc_tax
        else:
            debit = amount_rc_tax

        return {
            'name': self.number,
            'credit': credit,
            'debit': debit,
            'account_id': journal.default_credit_account_id.id,
            'company_id': self.company_id.id,
            }

    def rc_debit_line_vals(self, amount=None):
        credit = debit = 0.0

        if self.type == 'in_invoice':
            if amount:
                debit = amount
            else:
                debit = self.compute_rc_amount_tax()
        else:
            if amount:
                credit = amount
            else:
                credit = self.compute_rc_amount_tax()
        return {
            'name': self.number,
            'debit': debit,
            'credit': credit,
            'account_id': self.get_inv_line_to_reconcile().account_id.id,
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id
            }

    def rc_invoice_payment_vals(self, rc_type):
        return {
            'journal_id': rc_type.payment_journal_id.id,
            # 'period_id': self.period_id.id,
            'date': self.date,
            }

    def rc_payment_credit_line_vals(self, invoice):
        credit = debit = 0.0
        if invoice.type == 'out_invoice':
            credit = self.get_rc_inv_line_to_reconcile(invoice).debit
        else:
            debit = self.get_rc_inv_line_to_reconcile(invoice).credit
        return {
            'name': invoice.number,
            'credit': credit,
            'debit': debit,
            'account_id': self.get_rc_inv_line_to_reconcile(
                invoice).account_id.id,
            'partner_id': invoice.partner_id.id,
            'company_id': self.company_id.id
            }

    def rc_payment_debit_line_vals(self, invoice, journal):
        credit = debit = 0.0
        if invoice.type == 'out_invoice':
            debit = self.get_rc_inv_line_to_reconcile(invoice).debit
        else:
            credit = self.get_rc_inv_line_to_reconcile(invoice).credit
        return {
            'name': invoice.number,
            'debit': debit,
            'credit': credit,
            'account_id': journal.default_credit_account_id.id,
            'company_id': self.company_id.id
            }

    # def reconcile_supplier_invoice(self):
    #     rc_type = self.fiscal_position_id.rc_type_id
    #
    #     move_model = self.env['account.move']
    #     move_line_model = self.env['account.move.line']
    #
    #     rc_payment_data = self.rc_payment_vals(rc_type)
    #     rc_invoice = self.rc_self_invoice_id
    #     payment_credit_line_data = self.rc_payment_credit_line_vals(
    #         rc_invoice)
    #     payment_debit_line_data = self.rc_debit_line_vals(
    #         self.amount_total)
    #     # payment_credit_line_data['credit'])
    #     rc_payment_data['line_ids'] = [
    #         (0, 0, payment_debit_line_data),
    #         (0, 0, payment_credit_line_data),
    #     ]
    #     rc_payment = move_model.create(rc_payment_data)
    #     for move_line in rc_payment.line_ids:
    #         if move_line.debit:
    #             payment_debit_line = move_line
    #         elif move_line.credit:
    #             payment_credit_line = move_line
    #     rc_payment.post()
    #
    #     lines_to_rec = move_line_model.browse([
    #         self.get_inv_line_to_reconcile().id,
    #         payment_debit_line.id
    #     ])
    #     lines_to_rec.reconcile()
    #
    #     rc_lines_to_rec = move_line_model.browse([
    #         self.get_rc_inv_line_to_reconcile(rc_invoice).id,
    #         payment_credit_line.id
    #     ])
    #     rc_lines_to_rec.reconcile()

    def prepare_reconcile_supplier_invoice(self):
        rc_type = self.fiscal_position_id.rc_type_id
        move_model = self.env['account.move']
        rc_payment_data = self.rc_payment_vals(rc_type)
        rc_payment = move_model.create(rc_payment_data)

        payment_credit_line_data = self.rc_credit_line_vals(
            rc_type.payment_journal_id)

        payment_debit_line_data = self.rc_debit_line_vals()
        rc_payment.line_ids = [
            (0, 0, payment_debit_line_data),
            (0, 0, payment_credit_line_data),
        ]
        return rc_payment

    def partially_reconcile_supplier_invoice(self, rc_payment):
        move_line_model = self.env['account.move.line']
        payment_debit_line = None
        for move_line in rc_payment.line_ids:
            if move_line.account_id.internal_type == 'payable':
                if ((self.type == 'in_invoice' and move_line.debit) or
                        (self.type == 'in_refund' and move_line.credit)):
                    payment_debit_line = move_line
        inv_lines_to_rec = move_line_model.browse(
            [self.get_inv_line_to_reconcile().id,
                payment_debit_line.id])
        inv_lines_to_rec.reconcile()

    def reconcile_rc_invoice(self, rc_payment):
        rc_type = self.fiscal_position_id.rc_type_id
        move_line_model = self.env['account.move.line']
        rc_invoice = self.rc_self_invoice_id
        rc_payment_credit_line_data = self.rc_payment_credit_line_vals(
            rc_invoice)
        rc_payment_debit_line_data = self.rc_payment_debit_line_vals(
            rc_invoice, rc_type.payment_journal_id)

        rc_payment.line_ids = [
            (0, 0, rc_payment_debit_line_data),
            (0, 0, rc_payment_credit_line_data),
        ]
        inv_line_to_reconcile = self.get_rc_inv_line_to_reconcile(rc_invoice)
        for move_line in rc_payment.line_ids:
            if move_line.account_id.id == inv_line_to_reconcile.account_id.id:
                rc_payment_line_to_reconcile = move_line

        rc_lines_to_rec = move_line_model.browse(
            [inv_line_to_reconcile.id,
                rc_payment_line_to_reconcile.id])
        rc_lines_to_rec.reconcile()

    # richiamato da l10n_it_fatturapa_out_rc
    #
    def generate_self_invoice(self):
        # update fields
        if self.fiscal_position_id.rc_type and \
            self.fiscal_position_id.rc_type == 'self'\
            and self.fiscal_position_id.self_journal_id:

            if self.fiscal_position_id.partner_type == 'other':
                # partner
                rc_partner = self.company_id.partner_id
            elif self.fiscal_position_id.partner_type == 'supplier':
                rc_partner = self.partner_id
            else:
                raise UserError('Invalid partner: partner not set.')
            # self invoice
            rc_invoice_lines = []
            # creo la fattura in bozza
            #
            # IMPOSTAZIONI
            #
            # currency
            rc_currency = self.currency_id
            # account_id
            rc_account = rc_partner.property_account_receivable_id
            # journal_id
            journal_id = self.fiscal_position_id.self_journal_id
            # account_tax sale
            tax_with_sell = self._get_tax_sell()
            tax_sell_id = tax_with_sell.tax_line_id.rc_sale_tax_id.id

            #
            # righe RC
            #
            for line in self.invoice_line_ids:
                # se di reverse charge
                if line.rc:
                    rc_invoice_line = self.rc_inv_line_vals(line)
                    rc_invoice_line.update(
                        {
                            'account_id': rc_account.id
                        }
                    )

                    if tax_sell_id:
                        rc_invoice_line.update(
                            {
                                'invoice_line_tax_ids': [
                                    (6, False, [tax_sell_id])],
                            }
                        )
                    rc_invoice_lines.append([0, False, rc_invoice_line])

            if rc_invoice_lines:

                inv_vals = self.rc_inv_vals(
                    rc_partner, rc_account, journal_id, rc_invoice_lines,
                    rc_currency)

                # no copy values
                inv_vals['date'] = self.date
                inv_vals['date_apply_balance'] = self.date_apply_balance
                inv_vals['date_apply_vat'] = self.date_apply_vat
                inv_vals['date_due'] = self.date
                inv_vals['date_effective'] = self.date
                inv_vals['date_invoice'] = self.date
                inv_vals['fiscal_position'] = None
                # inv_vals['payment_term_id'] = self.payment_term_id.id

                if self.rc_self_invoice_id:
                    # this is needed when user takes back to draft supplier
                    # invoice, edit and validate again
                    rc_invoice = self.rc_self_invoice_id
                    rc_invoice.invoice_line_ids.unlink()
                    rc_invoice.period_id = False
                    rc_invoice.write(inv_vals)
                    rc_invoice.compute_taxes()
                    rc_invoice.duedate_manager_id.write_duedate_lines()
                else:
                    rc_invoice = self.create(inv_vals)
                    self.rc_self_invoice_id = rc_invoice.id

                rc_invoice.action_invoice_open()

                if rc_invoice.state == 'open':
                    # add credit line
                    credit_line = self.move_id.line_ids.filtered(
                        lambda
                            x: self.company_id.id == x.company_id.id and x.line_type == 'tax'
                               and rc_account.id == x.account_id.id and x.credit == self.amount_rc
                    )
                    rc_lines_to_rec = rc_invoice.move_id.line_ids.filtered(
                        lambda
                            x: rc_invoice.company_id.id == x.company_id.id
                               and rc_account.id == x.account_id.id
                    )

                    if credit_line:
                        rc_lines_to_rec += credit_line
                        rc_lines_to_rec.reconcile()

        if self.rc_self_invoice_id:
            if self.fatturapa_attachment_in_id:
                doc_id = self.fatturapa_attachment_in_id.name
            else:
                doc_id = self.reference if self.reference else self.number
            self.rc_self_invoice_id.related_documents = [
                (0, 0, {
                    "type": "invoice",
                    "name": doc_id,
                    "date": self.date_invoice,
                })
            ]

    # non tenere
    def generate_supplier_self_invoice(self):
        if self.fiscal_position_id.rc_type and \
            self.fiscal_position_id.rc_type == 'self' and \
            self.fiscal_position_id.partner_type == 'supplier':

            rc_partner = self.partner_id
            rc_currency = self.currency_id
            rc_account = rc_partner.property_account_receivable_id

            if not self.rc_self_purchase_invoice_id:
                supplier_invoice = self.copy()
            else:
                supplier_invoice_vals = self.copy_data()
                supplier_invoice = self.rc_self_purchase_invoice_id
                supplier_invoice.invoice_line_ids.unlink()
                supplier_invoice.write(supplier_invoice_vals[0])

            supplier_invoice.partner_bank_id = None

            # because this field has copy=False
            supplier_invoice.date = self.date
            supplier_invoice.date_invoice = self.date
            supplier_invoice.date_due = self.date
            supplier_invoice.partner_id = rc_partner.id
            # supplier_invoice.journal_id = rc_type.supplier_journal_id.id
            # for inv_line in supplier_invoice.invoice_line_ids:
            #     inv_line.invoice_line_tax_ids = [
            #         (6, 0, [rc_type.tax_ids[0].purchase_tax_id.id])]
            #     inv_line.account_id = rc_type.transitory_account_id.id
            self.rc_self_purchase_invoice_id = supplier_invoice.id

            # temporary disabling self invoice automations
            supplier_invoice.fiscal_position_id = None
            supplier_invoice.compute_taxes()
            supplier_invoice.check_total = supplier_invoice.amount_total
            supplier_invoice.action_invoice_open()
            supplier_invoice.fiscal_position_id = self.fiscal_position_id.id

    # @api.multi
    # def compute_taxes(self):
    #     res = super().compute_taxes()
    #     for inv in self:
    #         inv.amount_rc = inv.compute_rc_amount_tax()
    #     # end for
    #     return res
    # # end compute_taxes

    @api.multi
    def invoice_validate(self):
        """Invoice validation is called to validate sale self-invoice
        """
        res = super().invoice_validate()
        for invoice in self:
            # self.ensure_one()
            if invoice.fiscal_position_id.rc_type \
                and invoice.rc_type == 'self':
                invoice.generate_self_invoice()
            # end if
        return res

    # tenere?
    def remove_rc_payment(self):
        inv = self
        if inv.rc_type and inv.rc_type == 'self':
            # remove move reconcile related to the self invoice
            move = inv.rc_self_invoice_id.move_id
            rec_lines = move.mapped('line_ids').filtered(
                'full_reconcile_id'
            ).mapped('full_reconcile_id.reconciled_line_ids')
            rec_lines.remove_move_reconcile()
            # cancel self invoice
            self_invoice = self.browse(
                inv.rc_self_invoice_id.id)
            self_invoice.action_invoice_cancel()

        if inv.payment_move_line_ids:
            if len(inv.payment_move_line_ids) > 1:
                raise UserError(
                    _('There are more than one payment line.\n'
                      'In that case account entries cannot be canceled'
                      'automatically. Please proceed manually'))
            payment_move = inv.payment_move_line_ids[0].move_id

            move = inv.move_id
            rec_partial = move.mapped('line_ids').filtered(
                'matched_debit_ids').mapped('matched_debit_ids')
            rec_partial_lines = (
                rec_partial.mapped('credit_move_id') |
                rec_partial.mapped('debit_move_id')
            )
            rec_partial_lines.remove_move_reconcile()
            #
            # also remove full reconcile, in case of with_supplier_self_invoice
            rec_partial_lines = move.mapped('line_ids').filtered(
                'full_reconcile_id'
            ).mapped('full_reconcile_id.reconciled_line_ids')
            rec_partial_lines.remove_move_reconcile()

            # invalidate and delete the payment move generated
            # by the self invoice creation
            payment_move.button_cancel()
            payment_move.unlink()

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        # reverse charge vat for in.invoice / in.refund only
        if self.type == 'out_invoice' or self.type == 'out_refund':
            return res
        # end if
        for invoice in self:
            if invoice.fiscal_position_id.rc_type:
                posted = False
                transfer_ids = list()
                # self or local
                invoice_rc_type = invoice.fiscal_position_id.rc_type
                # journal used to reconcile
                journal_id = invoice.move_id.journal_id
                # back to draft
                if invoice.move_id.state == 'posted':
                    posted = True
                    invoice.move_id.state = 'draft'
                # end if
                line_model = self.env['account.move.line']

                # common

                tax_with_sell = invoice._get_tax_sell()
                tax_vat = tax_with_sell.tax_line_id
                tax_sell = tax_vat.rc_sale_tax_id

                tax_duedate_rc = invoice.move_id.line_ids.filtered(
                    lambda
                        x: x.account_id.id == invoice.account_id.id and x.credit == invoice.amount_rc and x.partner_id.id == invoice.partner_id.id and invoice.company_id.id == x.company_id.id)

                transfer_ids.append(tax_duedate_rc.id)

                if invoice_rc_type and invoice_rc_type == 'local':

                    # punto 7
                    vat_sell_vals = {
                        'name': 'Iva su vendite',
                        'partner_id': invoice.partner_id.id,
                        'account_id': tax_sell.account_id.id,
                        'journal_id': journal_id.id,
                        'date': invoice.date,
                        'debit': 0,
                        'credit': invoice.amount_rc,
                        'tax_line_id': tax_sell.id,
                        'move_id': invoice.move_id.id,
                    }
                    if invoice.type == 'in_refund':
                        vat_sell_vals['credit'] = 0
                        vat_sell_vals['debit'] = invoice.amount_rc

                    sell = line_model.with_context(
                        {'check_move_validity': False}
                    ).create(vat_sell_vals)

                    # punto 8
                    # reconcile with tax_duedate
                    supplier_vat_vals = {
                        'name': 'Fornitore Iva RC',
                        'partner_id': invoice.partner_id.id,
                        'account_id': invoice.account_id.id,
                        'journal_id': journal_id.id,
                        'date': invoice.date,
                        'debit': invoice.amount_rc,
                        'credit': 0,
                        'tax_line_id': tax_vat.id,
                        'move_id': invoice.move_id.id,
                    }
                    if invoice.type == 'in_refund':
                        supplier_vat_vals['debit'] = 0
                        supplier_vat_vals['credit'] = invoice.amount_rc

                    tranfer = line_model.with_context(
                        check_move_validity=False
                    ).create(supplier_vat_vals)

                    transfer_ids.append(tranfer.id)

                elif invoice_rc_type and invoice_rc_type == 'self':

                    # punto 5
                    if invoice.fiscal_position_id.partner_type == 'supplier':
                        partner_id = invoice.partner_id
                    elif invoice.fiscal_position_id.partner_type == 'other':
                        partner_id = invoice.company_id.partner_id
                    else:
                        raise UserError('Anomalia partner')
                    # end if

                    vat_sell_vals = {
                        'name': 'Iva su vendite',
                        'partner_id': partner_id.id,
                        'account_id':
                            partner_id.property_account_receivable_id.id,
                        'journal_id': journal_id.id,
                        'date': invoice.date,
                        'debit': 0,
                        'credit': invoice.amount_rc,
                        'tax_line_id': tax_sell.id,
                        'move_id': invoice.move_id.id,
                    }
                    if invoice.type == 'in_refund':
                        vat_sell_vals['credit'] = 0
                        vat_sell_vals['debit'] = invoice.amount_rc

                    sell = line_model.with_context(
                        {'check_move_validity': False}
                    ).create(vat_sell_vals)

                    # punto 6
                    # reconcile with tax_duedate
                    supplier_vat_vals = {
                        'name': 'Fornitore Iva RC',
                        'partner_id': invoice.partner_id.id,
                        'account_id': invoice.account_id.id,
                        'journal_id': journal_id.id,
                        'date': invoice.date,
                        'debit': invoice.amount_rc,
                        'credit': 0,
                        'payment_method': tax_duedate_rc.payment_method.id,
                        'move_id': invoice.move_id.id,
                    }
                    if invoice.type == 'in_refund':
                        supplier_vat_vals['debit'] = 0
                        supplier_vat_vals['credit'] = invoice.amount_rc

                    tranfer = line_model.with_context(
                        check_move_validity=False
                    ).create(supplier_vat_vals)

                    transfer_ids.append(tranfer.id)
                # end if

                # reconcile
                if tax_duedate_rc and tax_duedate_rc.id:
                    lines_to_rec = line_model.browse(transfer_ids)
                    lines_to_rec.reconcile()

                if posted:
                    invoice.move_id.state = 'posted'
                invoice._compute_residual()
            # end if
        return res
    # end action_move_create

    @api.multi
    def action_cancel(self):
        for inv in self:
            rc_type = inv.fiscal_position_id.rc_type
            if (
                rc_type and
                rc_type == 'self' and
                inv.rc_self_invoice_id
            ):
                inv.remove_rc_payment()

        return super(AccountInvoice, self).action_cancel()

    @api.multi
    def action_invoice_draft(self):
        new_self = self.with_context(rc_set_to_draft=True)
        super(AccountInvoice, new_self).action_invoice_draft()
        invoice_model = new_self.env['account.invoice']
        for inv in new_self:
            if inv.rc_self_invoice_id:
                self_invoice = invoice_model.browse(
                    inv.rc_self_invoice_id.id)
                self_invoice.action_cancel()
                self_invoice.action_invoice_draft()
            # if inv.rc_self_purchase_invoice_id:
            #     self_purchase_invoice = invoice_model.browse(
            #         inv.rc_self_purchase_invoice_id.id)
            #     self_purchase_invoice.action_invoice_draft()
        return True

    # modulo dipendenza
    def get_tax_amount_added_for_rc(self):
        res = 0
        for line in self.invoice_line_ids:
            if line.rc:
                price_unit = line.price_unit * (
                    1 - (line.discount or 0.0) / 100.0)
                taxes = line.invoice_line_tax_ids.compute_all(
                    price_unit, self.currency_id, line.quantity,
                    line.product_id, self.partner_id)['taxes']
                for tax in taxes:
                    res += tax['amount']
        return res

    def _get_tax_sell(self):
        return self.move_id.line_ids.filtered(
            lambda
                x: self.company_id.id == x.company_id.id and x.line_type == 'tax' and x.debit == self.amount_rc)
    # end _get_tax_sell

    # ------------------------------------------------------------------------#
    #  FROM l10n_it_fatturapa_in_rc                                          #
    # ------------------------------------------------------------------------#

    def e_inv_check_amount_tax(self):
        if (
            any(self.invoice_line_ids.mapped('rc')) and
            self.e_invoice_amount_tax
        ):
            error_message = ''
            amount_added_for_rc = self.get_tax_amount_added_for_rc()
            amount_tax = self.amount_tax - amount_added_for_rc
            if float_compare(
                amount_tax, self.e_invoice_amount_tax,
                precision_rounding=self.currency_id.rounding
            ) != 0:
                error_message = (
                    _("Taxed amount ({bill_amount_tax}) "
                      "does not match with "
                      "e-bill taxed amount ({e_bill_amount_tax})")
                    .format(
                        bill_amount_tax=amount_tax or 0,
                        e_bill_amount_tax=self.e_invoice_amount_tax
                    ))
            return error_message
        else:
            return super(AccountInvoice, self).e_inv_check_amount_tax()

    def e_inv_check_amount_total(self):
        if (
            any(self.invoice_line_ids.mapped('rc')) and
            self.e_invoice_amount_total
        ):
            error_message = ''
            amount_added_for_rc = self.get_tax_amount_added_for_rc()
            amount_total = self.amount_total - amount_added_for_rc
            if float_compare(
                amount_total, self.e_invoice_amount_total,
                precision_rounding=self.currency_id.rounding
            ) != 0:
                error_message = (
                    _("Total amount ({bill_amount_total}) "
                      "does not match with "
                      "e-bill total amount ({e_bill_amount_total})")
                    .format(
                        bill_amount_total=amount_total or 0,
                        e_bill_amount_total=self.e_invoice_amount_total
                    ))
            return error_message
        else:
            return super(AccountInvoice, self).e_inv_check_amount_total()

