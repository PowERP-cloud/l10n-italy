# Copyright 2021-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2021-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021-22 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#

from odoo import api, fields, models
from odoo.exceptions import Warning as UserError
from odoo.tools import float_compare
from odoo.tools.translate import _


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
        if invoice.type in ["in_invoice", "in_refund"]:
            for tax in self.invoice_line_tax_ids:
                if tax.rc_type:
                    self.rc = True
                else:
                    self.rc = False
                # end if
            # end for
        # end fi

    # end _set_rc_flag

    @api.onchange("invoice_line_tax_ids")
    def onchange_invoice_line_tax_id(self):
        res = dict()
        invoice_rc_type = self.invoice_id.fiscal_position_id.rc_type
        if self.invoice_id.type in ["in_invoice", "in_refund",] and invoice_rc_type in [
            "local",
            "self",
        ]:
            for tax in self.invoice_line_tax_ids:
                if not tax.rc_type:
                    raise UserError(
                        _("Tipo RC non impostato per il codice IVA %s.")
                        % tax.description
                    )

                if tax.rc_type != invoice_rc_type:
                    raise UserError(
                        _(
                            "Tipo RC %s di codice IVA %s "
                            "non valida per reverse charge."
                        )
                        % tax.rc_type,
                        tax.description,
                    )
        if not res:
            self._set_rc_flag(self.invoice_id)
        # end if
        return res

    rc = fields.Boolean("RC")

    line_rc_type = fields.Boolean("Has RC", compute="compute_rc_type")

    def _set_additional_fields(self, invoice):
        self._set_rc_flag(invoice)
        return super(AccountInvoiceLine, self)._set_additional_fields(invoice)


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.depends("invoice_line_ids")
    def _compute_amount_rc(self):
        for inv in self:
            (
                inv.amount_rc_company_currency,
                inv.amount_rc,
            ) = inv.compute_rc_amount_tax()
        # end for

    # end _compute_amount_rc

    @api.depends("fiscal_position_id")
    def _compute_rc_type(self):
        for inv in self:
            inv.rc_type = inv.fiscal_position_id.rc_type
        # end for

    # end _compute_rc_type

    @api.depends("amount_total", "amount_rc")
    def _compute_net_pay(self):
        super()._compute_net_pay()
        for inv in self:
            if inv.fiscal_position_id.rc_type:
                inv.amount_net_pay = inv.amount_total - inv.amount_rc
        # end for

    # end _compute_net_pay

    rc_self_invoice_id = fields.Many2one(
        comodel_name="account.invoice",
        string="RC Self Invoice",
        copy=False,
        readonly=True,
    )
    rc_purchase_invoice_id = fields.Many2one(
        comodel_name="account.invoice",
        string="RC Purchase Invoice",
        copy=False,
        readonly=True,
    )
    rc_self_purchase_invoice_id = fields.Many2one(
        comodel_name="account.invoice",
        string="RC Self Purchase Invoice",
        copy=False,
        readonly=True,
    )
    # Invoice currency RC amount
    amount_rc = fields.Monetary(
        string="RC Tax",
        currency_field="currency_id",
        store=True,
        readonly=True,
        compute="_compute_amount_rc",
    )
    # Company currency RC amount
    amount_rc_company_currency = fields.Monetary(
        string="RC Tax in Company Currency",
        currency_field="company_currency_id",
        store=True,
        readonly=True,
        compute="_compute_amount_rc",
    )
    rc_type = fields.Char(
        string="RC Type",
        compute="_compute_rc_type",
    )
    # show_reload_tax = fields.Boolean(readonly=True, default=False, copy=False,)

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

        stop_recursion = self.env.context.get("StopRecursion", False)

        if not stop_recursion:
            # Enable stop recursion
            self = self.with_context(StopRecursion=True)

            for inv in self:
                if inv.rc_type:
                    (
                        inv.amount_rc_company_currency,
                        inv.amount_rc,
                    ) = inv.compute_rc_amount_tax()
            # end for
        # end if
        return result

    # end write

    @api.onchange("invoice_line_ids")
    def _onchange_invoice_line_ids(self):
        super()._onchange_invoice_line_ids()
        for line in self.invoice_line_ids:
            line._set_rc_flag(self)

    @api.onchange("fiscal_position_id")
    def onchange_rc_fiscal_position_id(self):
        for line in self.invoice_line_ids:
            line._set_rc_flag(self)

    @api.onchange("partner_id", "company_id")
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
        # In some cases (like creating the invoice from PO),
        # fiscal position's onchange is triggered
        # before than being changed by this method.
        self.onchange_rc_fiscal_position_id()
        return res

    @api.multi
    def taxes_reload(self):
        for invoice in self:
            if invoice.state == "draft":
                res = invoice.compute_taxes()
        return res

    # end taxes_reload

    # tenere
    def _compute_amount(self):
        super()._compute_amount()
        for inv in self:
            if inv.rc_type:
                inv.amount_total = inv.amount_untaxed + inv.amount_tax
                if inv.rc_type in ("self", "local"):
                    inv.amount_tax -= inv.amount_rc
                # end if
            # end if

    # end _compute_amount

    def rc_inv_line_vals(self, line):
        return {
            "product_id": line.product_id.id,
            "name": line.name,
            "uom_id": line.product_id.uom_id.id,
            "price_unit": line.price_unit,
            "quantity": line.quantity,
            "discount": line.discount,
        }

    def rc_inv_vals(self, partner, account, journal_id, lines, currency):
        inv_vals = {
            "partner_id": partner.id,
            "account_id": account.id,
            "journal_id": journal_id.id,
            "type": {
                # 'in_invoice': 'out_invoice',
                "in_refund": "out_refund",
            }.get(self.type, "out_invoice"),
            "date_due": self.date_invoice,
            # Warning! Do not change follow statement!
            # In sale invoice, date is automatically set to date_invoice
            "date_invoice": self.date_invoice if journal_id.rev_charge else self.date,
            "origin": self.number,
            "rc_purchase_invoice_id": self.id,
            "name": _("Reverse charge self invoice"),
            "currency_id": currency.id,
            "fiscal_position_id": False,
            "payment_term_id": False,
            "invoice_line_ids": lines,
        }
        for field in ("date", "date_apply_balance", "date_apply_vat", "date_effective"):
            if hasattr(self, field):
                inv_vals[field] = getattr(self, field)

        inv_vals["comment"] = _(
            "Reverse charge self invoice.\n"
            "Supplier: %s\n"
            "Reference: %s\n"
            "Date: %s\n"
            "Internal reference: %s"
        ) % (
            self.partner_id.display_name,
            self.reference or "",
            self.date,
            self.number,
        )
        return inv_vals

    def get_inv_line_to_reconcile(self):
        for inv_line in self.move_id.line_ids:
            if (self.type == "in_invoice") and inv_line.credit:
                return inv_line
            elif (self.type == "in_refund") and inv_line.debit:
                return inv_line
        return False

    def get_rc_inv_line_to_reconcile(self, invoice):
        for inv_line in invoice.move_id.line_ids:
            if (invoice.type == "out_invoice") and inv_line.debit:
                return inv_line
            elif (invoice.type == "out_refund") and inv_line.credit:
                return inv_line
        return False

    def rc_payment_vals(self, rc_type):
        return {
            "journal_id": rc_type.payment_journal_id.id,
            # 'period_id': self.period_id.id,
            "date": self.date,
        }

    def compute_rc_amount_tax(self):
        """Compute RC amount: return company and invoice currency amounts"""
        rc_amount_tax = 0.0
        round_curr = self.currency_id.round
        rc_lines = self.invoice_line_ids.filtered(lambda l: l.rc)
        for rc_line in rc_lines:
            price_unit = rc_line.price_unit * (1 - (rc_line.discount or 0.0) / 100.0)
            taxes = rc_line.invoice_line_tax_ids.compute_all(
                price_unit,
                self.currency_id,
                rc_line.quantity,
                product=rc_line.product_id,
                partner=rc_line.partner_id,
            )["taxes"]
            rc_amount_tax += sum([tax["amount"] for tax in taxes])

        # convert the amount to main company currency, as
        # compute amount_rc_tax_company_currency, used for debit/credit fields
        invoice_currency = self.currency_id.with_context(date=self.date_invoice)
        main_currency = self.company_currency_id.with_context(date=self.date_invoice)
        amount_rc_tax_company_currency = rc_amount_tax
        if invoice_currency != main_currency:
            amount_rc_tax_company_currency = invoice_currency.compute(
                rc_amount_tax, main_currency
            )
        return (
            main_currency.round(amount_rc_tax_company_currency),
            round_curr(rc_amount_tax),
        )

    def template_rc_line(
        self,
        side,
        account_id=None,
        partner_id=None,
        amount=None,
        amount_company_currency=None,
    ):
        """Load dictionary for rc line
        Args:
            side(str): line side, 'debit' or 'credit'
        """
        if side not in ("debit", "credit"):
            raise UserError(_("Internal error: invalid debit/credit side"))
        opposite_side = {"debit": "credit", "credit": "debit"}[side]
        if amount:
            amount_rc_tax = amount
            amount_rc_tax_company_currency = amount_company_currency or amount
        else:
            (
                amount_rc_tax_company_currency,
                amount_rc_tax,
            ) = self.compute_rc_amount_tax()
        vals = {
            side: amount_rc_tax_company_currency,
            opposite_side: 0.0,
            "company_id": self.company_id.id,
            "partner_id": partner_id or self.partner_id.id,
            "name": self.number,
            "date": self.date,
        }
        if self.currency_id:
            vals["currency_id"] = self.currency_id.id
            if side == "debit":
                vals["amount_currency"] = amount_rc_tax
            else:
                vals["amount_currency"] = -amount_rc_tax
        if account_id:
            vals["account_id"] = account_id
        if self.move_id:
            vals["move_id"] = self.move_id.id
            if self.move_id.journal_id:
                vals["journal_id"] = self.move_id.journal_id.id
        return vals

    def rc_credit_line_vals(self, journal):
        return self.template_rc_line(
            "credit" if self.type == "in_invoice" else "debit",
            account_id=journal.default_credit_account_id.id,
        )

    def rc_debit_line_vals(self, amount=None):
        return self.template_rc_line(
            "debit" if self.type == "in_invoice" else "credit",
            account_id=self.get_inv_line_to_reconcile().account_id.id,
            amount=amount,
        )

    def rc_invoice_payment_vals(self, rc_type):
        return {
            "journal_id": rc_type.payment_journal_id.id,
            # 'period_id': self.period_id.id,
            "date": self.date,
        }

    def rc_payment_credit_line_vals(self, invoice):
        credit = debit = 0.0
        if invoice.type == "out_invoice":
            credit = self.get_rc_inv_line_to_reconcile(invoice).debit
        else:
            debit = self.get_rc_inv_line_to_reconcile(invoice).credit
        return {
            "name": invoice.number,
            "credit": credit,
            "debit": debit,
            "account_id": self.get_rc_inv_line_to_reconcile(invoice).account_id.id,
            "partner_id": invoice.partner_id.id,
            "company_id": self.company_id.id,
        }

    def rc_payment_debit_line_vals(self, invoice, journal):
        credit = debit = 0.0
        if invoice.type == "out_invoice":
            debit = self.get_rc_inv_line_to_reconcile(invoice).debit
        else:
            credit = self.get_rc_inv_line_to_reconcile(invoice).credit
        return {
            "name": invoice.number,
            "debit": debit,
            "credit": credit,
            "account_id": journal.default_credit_account_id.id,
            "company_id": self.company_id.id,
        }

    def partially_reconcile_supplier_invoice(self, rc_payment):
        move_line_model = self.env["account.move.line"]
        payment_debit_line = None
        for move_line in rc_payment.line_ids:
            if move_line.account_id.internal_type == "payable":
                if (self.type == "in_invoice" and move_line.debit) or (
                    self.type == "in_refund" and move_line.credit
                ):
                    payment_debit_line = move_line
        inv_lines_to_rec = move_line_model.browse(
            [self.get_inv_line_to_reconcile().id, payment_debit_line.id]
        )
        inv_lines_to_rec.reconcile()

    #
    # richiamato da l10n_it_fatturapa_out_rc
    #
    def generate_self_invoice(self):
        # update fields
        if (
            self.fiscal_position_id.rc_type
            and self.fiscal_position_id.rc_type == "self"
        ):
            if (
                self.fiscal_position_id.self_journal_id
                and self.fiscal_position_id.self_journal_id.id
            ):
                # journal_id
                journal_id = self.fiscal_position_id.self_journal_id
            else:
                raise UserError(
                    "Configurazione mancante nella "
                    "posizione fiscale: Registro per autofattura"
                )

            if self.fiscal_position_id.partner_type == "other":
                # partner
                rc_partner = self.company_id.partner_id
            elif self.fiscal_position_id.partner_type == "supplier":
                rc_partner = self.partner_id
            else:
                raise UserError(
                    "Configurazione mancante nella "
                    "posizione fiscale: Tipo di partner"
                )

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
            # end if

            #
            # righe RC
            #
            for line in self.invoice_line_ids:
                # se di reverse charge
                if line.rc:

                    tax_sell_id = line.invoice_line_tax_ids.rc_sale_tax_id.id

                    rc_invoice_line = self.rc_inv_line_vals(line)
                    rc_invoice_line.update({"account_id": rc_account.id})

                    if tax_sell_id:
                        rc_invoice_line.update(
                            {
                                "invoice_line_tax_ids": [(6, False, [tax_sell_id])],
                            }
                        )
                    rc_invoice_lines.append([0, False, rc_invoice_line])

            if rc_invoice_lines:

                inv_vals = self.rc_inv_vals(
                    rc_partner,
                    rc_account,
                    journal_id,
                    rc_invoice_lines,
                    rc_currency,
                )

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

                if self.fiscal_position_id.rc_fiscal_document_type_id:
                    fid = self.fiscal_position_id.rc_fiscal_document_type_id
                    rc_invoice.fiscal_document_type_id = fid.id

                rc_invoice.action_invoice_open()

                if self.type == "in_refund":
                    debit_line = self.move_id.line_ids.filtered(
                        lambda x: self.company_id.id == x.company_id.id
                        # and x.line_type == 'tax'
                        and rc_account.id == x.account_id.id
                    )

                    rc_lines_to_rec = rc_invoice.move_id.line_ids.filtered(
                        lambda x: rc_invoice.company_id.id == x.company_id.id
                        and rc_account.id == x.account_id.id
                    )

                    if debit_line:
                        rc_lines_to_rec += debit_line
                        rc_lines_to_rec.reconcile()
                    # end if

                else:
                    credit_line = self.move_id.line_ids.filtered(
                        lambda x: self.company_id.id == x.company_id.id
                        # and x.line_type == 'tax'
                        and rc_account.id == x.account_id.id
                        # and x.credit == self.amount_rc
                    )
                    rc_lines_to_rec = rc_invoice.move_id.line_ids.filtered(
                        lambda x: rc_invoice.company_id.id == x.company_id.id
                        and rc_account.id == x.account_id.id
                    )

                    if credit_line:
                        rc_lines_to_rec += credit_line
                        rc_lines_to_rec.reconcile()
                    # end if
                # end if

        if self.rc_self_invoice_id:
            if self.fatturapa_attachment_in_id:
                doc_id = self.fatturapa_attachment_in_id.name
            else:
                doc_id = self.reference if self.reference else self.number
            # end if
            self.rc_self_invoice_id.related_documents = [
                (
                    0,
                    0,
                    {
                        "type": "invoice",
                        "name": doc_id,
                        "date": self.date_invoice,
                    },
                )
            ]

        # end if

    @api.multi
    def invoice_validate(self):
        """Invoice validation is called to validate sale self-invoice"""
        res = super().invoice_validate()
        for invoice in self:
            # self.ensure_one()
            if invoice.fiscal_position_id.rc_type and invoice.rc_type == "self":
                invoice.generate_self_invoice()
                # end if
            # end if
        return res

    # tenere?
    def remove_rc_payment(self):
        inv = self
        if inv.rc_type and inv.rc_type == "self":
            # remove move reconcile related to the self invoice
            move = inv.rc_self_invoice_id.move_id
            rec_lines = (
                move.mapped("line_ids")
                .filtered("full_reconcile_id")
                .mapped("full_reconcile_id.reconciled_line_ids")
            )
            rec_lines.remove_move_reconcile()
            # cancel self invoice
            self_invoice = self.browse(inv.rc_self_invoice_id.id)
            self_invoice.action_invoice_cancel()

        if inv.payment_move_line_ids:
            if len(inv.payment_move_line_ids) > 1:
                raise UserError(
                    _(
                        "There are more than one payment line.\n"
                        "In that case account entries cannot be canceled"
                        "automatically. Please proceed manually"
                    )
                )
            payment_move = inv.payment_move_line_ids[0].move_id

            move = inv.move_id
            rec_partial = (
                move.mapped("line_ids")
                .filtered("matched_debit_ids")
                .mapped("matched_debit_ids")
            )
            rec_partial_lines = rec_partial.mapped(
                "credit_move_id"
            ) | rec_partial.mapped("debit_move_id")
            rec_partial_lines.remove_move_reconcile()
            #
            # also remove full reconcile, in case of with_supplier_self_invoice
            rec_partial_lines = (
                move.mapped("line_ids")
                .filtered("full_reconcile_id")
                .mapped("full_reconcile_id.reconciled_line_ids")
            )
            rec_partial_lines.remove_move_reconcile()

            # invalidate and delete the payment move generated
            # by the self invoice creation
            payment_move.button_cancel()
            payment_move.unlink()

    @api.multi
    def action_move_create(self):
        """Add some lines to account move to manage reverse-charge entry
        We consider 2 types of reverse-charge:
        - local: invoice from domestic supplier
        - self: invoice from foreign supplier
        *local*
        Total invoice amount includes tax amount but tax amount must be
        reconciled with an invoice line;
        we create 2 new lines with RC tax amount
        +-----------+--------+--------+-------------------------------------+
        | Account   | Debit  | Credit | Notes                               |
        +-----------+--------+--------+-------------------------------------+
        | supplier  |        |    100 | By Odoo account module              |
        | expense   |    100 |        | By Odoo account module (tax code)   |
        | tax       |     22 |        | By Odoo account module (is tax)     |
        +-----------+--------+--------+-------------------------------------+
        | supplier  |        |     22 | Separated by duedate module (*)     |
        +-----------+--------+--------+-------------------------------------+
        | supplier! |     22 |        | Reconcile with (*) (is tax)         |
        | sale tax  |        |     22 | is tax code                         |
        +-----------+--------+--------+-------------------------------------+

        *self*
        Total invoice is without amount but ww had to add and refund tax amount
        +-----------+--------+--------+-------------------------------------+
        | Account   | Debit  | Credit | Notes                               |
        +-----------+--------+--------+-------------------------------------+
        | supplier  |        |    100 | By Odoo account module              |
        | expense   |    100 |        | By Odoo account module (tax code)   |
        | tax       |     22 |        | By Odoo account module (is tax)     |
        +-----------+--------+--------+-------------------------------------+
        | supplier  |        |     22 | Separated by duedate module (*)     |
        +-----------+--------+--------+-------------------------------------+
        | supplier  |     22 |        | Reconcile with (*)                  |
        | customer  |        |     22 | is tax code: partner may be company |
        +-----------+--------+--------+-------------------------------------+

        *self-x* (no yet implemented)
        Total invoice is without amount but ww had to add and refund tax amount
        +-----------+--------+--------+-------------------------------------+
        | Account   | Debit  | Credit | Notes                               |
        +-----------+--------+--------+-------------------------------------+
        | supplier  |        |    100 | By Odoo account module              |
        | expense   |    100 |        | By Odoo account module (tax code)   |
        +-----------+--------+--------+-------------------------------------+
        | supplier  |        |     22 | (*)                                 |
        | tax       |     22 |        |                                     |
        | supplier  |     22 |        | Reconcile with (*)                  |
        | customer  |        |     22 | is tax code: partner may be company |
        +-----------+--------+--------+-------------------------------------+
        """
        res = super(AccountInvoice, self).action_move_create()
        for invoice in self:
            # reverse charge vat for in.invoice / in.refund only
            if (
                invoice.type not in ("in_invoice", "in_refund")
                or not invoice.fiscal_position_id.rc_type
            ):
                continue

            line2reconcile_ids = self.env["account.move.line"]
            invoice_rc_type = invoice.fiscal_position_id.rc_type
            # journal used to reconcile
            # journal_id = invoice.move_id.journal_id
            # back to draft
            posted = False
            if invoice.move_id.state == "posted":
                posted = True
                invoice.move_id.state = "draft"
            # end if
            line_model = self.env["account.move.line"]

            line_with_rc_tax = invoice._get_line_with_rc_tax()
            if not line_with_rc_tax:
                msg = (
                    "Nessuna riga nella fattura con IVA reverse charge.\n"
                    "Cambiare posizione fiscale oppure inserire "
                    "un codice IVA inerente il reverse charge\n"
                    "e riaggiornare le imposte"
                )
                raise UserError(msg)
            # end if

            tax_rc = line_with_rc_tax.tax_line_id
            tax_rc_name = tax_rc.display_name or tax_rc.decription
            tax_rc_sale = tax_rc.rc_sale_tax_id
            if not tax_rc_sale:
                raise UserError(
                    "Codice iva vendite non impostato nella imposta "
                    "{tax}.".format(tax=tax_rc_name)
                )
            # end if

            # Search for payable line created by duedate module
            if invoice.type == "in_refund":
                line_duedate_rc = invoice.move_id.line_ids.filtered(
                    lambda x: x.account_id.id == invoice.account_id.id
                    and (
                        x.debit == invoice.amount_rc_company_currency
                        or x.amount_currency == invoice.amount_rc
                    )
                    and x.partner_id.id == invoice.partner_id.id
                    and invoice.company_id.id == x.company_id.id
                )
                amount_rc_company_currency = line_duedate_rc["debit"]
            else:
                line_duedate_rc = invoice.move_id.line_ids.filtered(
                    lambda x: x.account_id.id == invoice.account_id.id
                    and (
                        x.credit == invoice.amount_rc_company_currency
                        or x.amount_currency == -invoice.amount_rc
                    )
                    and x.partner_id.id == invoice.partner_id.id
                    and invoice.company_id.id == x.company_id.id
                )
                amount_rc_company_currency = line_duedate_rc["credit"]
            if not line_duedate_rc:
                raise UserError(_("Internal error: no rc line found!"))
            # Avoid round difference
            if (
                abs(amount_rc_company_currency - invoice.amount_rc_company_currency)
                >= 1.0
            ):
                amount_rc_company_currency = invoice.amount_rc_company_currency
            line2reconcile_ids += line_duedate_rc

            if invoice_rc_type == "local":
                tax_rc_sale_vals = invoice.template_rc_line(
                    "debit" if invoice.type == "in_refund" else "credit",
                    account_id=tax_rc_sale.account_id.id,
                    amount=invoice.amount_rc,
                    amount_company_currency=amount_rc_company_currency,
                )
                tax_rc_sale_vals["name"] = "Iva su vendite"
                tax_rc_sale_vals["tax_line_id"] = tax_rc_sale.id

                supplier_vat_vals = self.template_rc_line(
                    "credit" if invoice.type == "in_refund" else "debit",
                    account_id=invoice.account_id.id,
                    amount=invoice.amount_rc,
                    amount_company_currency=amount_rc_company_currency,
                )
                supplier_vat_vals["name"] = "Fornitore Iva RC"
                supplier_vat_vals["tax_line_id"] = tax_rc.id

            elif invoice_rc_type == "self":

                if invoice.fiscal_position_id.partner_type == "supplier":
                    self_partner = invoice.partner_id
                elif invoice.fiscal_position_id.partner_type == "other":
                    self_partner = invoice.company_id.partner_id
                else:
                    raise UserError(
                        "Configurazione mancante nella "
                        "posizione fiscale: Tipo di partner"
                    )
                # end if

                tax_rc_sale_vals = self.template_rc_line(
                    "debit" if invoice.type == "in_refund" else "credit",
                    account_id=self_partner.property_account_receivable_id.id,
                    partner_id=self_partner.id,
                    amount=invoice.amount_rc,
                    amount_company_currency=amount_rc_company_currency,
                )
                tax_rc_sale_vals["name"] = "Iva su vendite"
                tax_rc_sale_vals["tax_line_id"] = tax_rc_sale.id

                supplier_vat_vals = self.template_rc_line(
                    "credit" if invoice.type == "in_refund" else "debit",
                    account_id=invoice.account_id.id,
                    amount=invoice.amount_rc,
                    amount_company_currency=amount_rc_company_currency,
                )
                supplier_vat_vals["name"] = "Fornitore Iva RC"
            # end if

            line_model.with_context({"check_move_validity": False}).create(
                tax_rc_sale_vals
            )
            supplier_line = line_model.with_context(check_move_validity=False).create(
                supplier_vat_vals
            )
            if hasattr(line_model, "payment_method"):
                supplier_vat_vals["payment_method"] = line_duedate_rc.payment_method.id
            line2reconcile_ids += supplier_line
            if line_duedate_rc and line_duedate_rc.id:
                line2reconcile_ids.reconcile()

            if posted:
                invoice.move_id.state = "posted"
            invoice._compute_residual()
        return res

    # end action_move_create

    @api.multi
    def action_cancel(self):
        for inv in self:
            rc_type = inv.fiscal_position_id.rc_type
            if rc_type and rc_type == "self" and inv.rc_self_invoice_id:
                inv.remove_rc_payment()

        return super(AccountInvoice, self).action_cancel()

    @api.multi
    def action_invoice_draft(self):
        new_self = self.with_context(rc_set_to_draft=True)
        super(AccountInvoice, new_self).action_invoice_draft()
        invoice_model = new_self.env["account.invoice"]
        for inv in new_self:
            if inv.rc_self_invoice_id:
                self_invoice = invoice_model.browse(inv.rc_self_invoice_id.id)
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
                price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.invoice_line_tax_ids.compute_all(
                    price_unit,
                    self.currency_id,
                    line.quantity,
                    line.product_id,
                    self.partner_id,
                )["taxes"]
                for tax in taxes:
                    res += tax["amount"]
        return res

    def _get_line_with_rc_tax(self):
        return self.move_id.line_ids.filtered(
            lambda x: (
                self.company_id.id == x.company_id.id
                and x.line_type == "tax"
                and x.tax_line_id.rc_type
            )
        )

    # ------------------------------------------------------------------------#
    #  FROM l10n_it_fatturapa_in_rc                                          #
    # ------------------------------------------------------------------------#

    def e_inv_check_amount_tax(self):
        if any(self.invoice_line_ids.mapped("rc")) and self.e_invoice_amount_tax:
            error_message = ""
            amount_added_for_rc = self.get_tax_amount_added_for_rc()
            amount_tax = self.amount_tax - amount_added_for_rc
            if (
                float_compare(
                    amount_tax,
                    self.e_invoice_amount_tax,
                    precision_rounding=self.currency_id.rounding,
                )
                != 0
            ):
                error_message = _(
                    "Taxed amount ({bill_amount_tax}) "
                    "does not match with "
                    "e-bill taxed amount ({e_bill_amount_tax})"
                ).format(
                    bill_amount_tax=amount_tax or 0,
                    e_bill_amount_tax=self.e_invoice_amount_tax,
                )
            return error_message
        else:
            return super(AccountInvoice, self).e_inv_check_amount_tax()

    def e_inv_check_amount_total(self):
        if any(self.invoice_line_ids.mapped("rc")) and self.e_invoice_amount_total:
            error_message = ""
            amount_added_for_rc = self.get_tax_amount_added_for_rc()
            amount_total = self.amount_total - amount_added_for_rc
            if (
                float_compare(
                    amount_total,
                    self.e_invoice_amount_total,
                    precision_rounding=self.currency_id.rounding,
                )
                != 0
            ):
                error_message = _(
                    "Total amount ({bill_amount_total}) "
                    "does not match with "
                    "e-bill total amount ({e_bill_amount_total})"
                ).format(
                    bill_amount_total=amount_total or 0,
                    e_bill_amount_total=self.e_invoice_amount_total,
                )
            return error_message
        else:
            return super(AccountInvoice, self).e_inv_check_amount_total()
