#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    _DEFAULT_FINANCING_PCT = {
        "invoice_amount": 80,
        "taxable_amount": 100,
    }

    def _domain_effetti_allo_sconto(self):
        return [
            (
                "user_type_id",
                "in",
                [
                    self.env.ref("account.data_account_type_current_assets").id,
                    self.env.ref("account.data_account_type_receivable").id,
                    self.env.ref("account.data_account_type_liquidity").id
                ]
            )
        ]

    def _domain_effetti_presentati(self):
        return [
            (
                "user_type_id",
                "in",
                [
                    self.env.ref("account.data_account_type_current_assets").id,
                    self.env.ref("account.data_account_type_liquidity").id
                ]
            )
        ]

    def _domain_portafoglio_sbf(self):
        return [
            (
                "user_type_id",
                "in",
                [
                    self.env.ref("account.data_account_type_current_liabilities").id,
                    self.env.ref("account.data_account_type_liquidity").id
                ]
            )
        ]

    def _domain_expenses_account(self):
        return [
            (
                "user_type_id",
                "in",
                [
                    self.env.ref("account.data_account_type_expenses").id,
                    self.env.ref("account.data_account_type_direct_costs").id
                ]
            )
        ]

    def _domain_sezionale(self):
        return [
            (
                "type",
                "in",
                ["bank", "general"]
            ),
        ]

    def _domain_main_sezionale(self):
        return [
            (
                "type",
                "in",
                ["bank", "cash"]
            ),
            ("is_wallet", "=", False),
        ]

    @api.depends("portafoglio_sbf")
    def _importo_effetti(self):
        for rec in self:
            if rec.portafoglio_sbf and rec.portafoglio_sbf.id:
                query_select_account_balance = """
                 SELECT
                    SUM(debit) - SUM(credit) as balance
                    FROM account_move_line, account_move
                    WHERE account_move_line.account_id = {account_id}
                    and account_move_line.move_id = account_move.id
                    and account_move.state = 'posted'
                """.format(
                    # account_id=rec.effetti_allo_sconto.id
                    account_id=rec.portafoglio_sbf.id
                )

                self.env.cr.execute(query_select_account_balance)

                anticipo = [r[0] for r in self.env.cr.fetchall()]
                rec.importo_effetti_sbf = anticipo[0]
            else:
                rec.importo_effetti_sbf = 0.0

    @api.depends("portafoglio_sbf")
    def _impegno_effetti(self):
        for rec in self:
            if rec.portafoglio_sbf and rec.portafoglio_sbf.id:
                query_select_account_balance = """
                SELECT
                    SUM(debit) - SUM(credit) as balance
                    FROM account_move_line, account_move
                    WHERE (account_move_line.account_id = {account_id}
                    and account_move_line.move_id = account_move.id
                    and account_move.state <> 'posted')
                """.format(
                    account_id=rec.portafoglio_sbf.id,
                )

                self.env.cr.execute(query_select_account_balance)

                impegno = [r[0] for r in self.env.cr.fetchall()]
                rec.impegno_effetti_sbf = impegno[0]
            else:
                rec.impegno_effetti_sbf = 0.0
            # end if
        # end for

    # end _impegno_effetti

    @api.depends("limite_effetti_sbf", "importo_effetti_sbf")
    def _disponibilita_effetti(self):
        for bank in self:
            if bank.wallet_ids:
                residuo = 0.0
                for wallet in bank.wallet_ids:
                    wallet._disponibilita_effetti()
                    residuo += wallet.disponibilita_effetti_sbf
            else:
                residuo = bank.limite_effetti_sbf + (
                    bank.importo_effetti_sbf + bank.impegno_effetti_sbf
                )

            if residuo > 0:
                bank.disponibilita_effetti_sbf = residuo
            else:
                bank.disponibilita_effetti_sbf = 0.0

    def _set_main_bank_account_id_default(self):
        return self.env["account.journal"]

    # end _set_main_bank_account_id_default

    def _set_wallet_ids_default(self):
        domain = [
            ("type", "in", ["bank", "cash"]),
            ("is_wallet", "=", True),
            ("main_bank_account_id", "=", self.id),
        ]

        return self.search(domain)

    # end _set_wallet_ids_default

    def is_wallet_default(self):
        if self.bank_account_id:
            return self.bank_account_id.bank_is_wallet
        else:
            return False
        # end if

    # end is_wallet_default

    @api.depends("wallet_ids")
    def _has_children(self):
        if self.wallet_ids:
            self.has_children = True
        else:
            self.has_children = False
        # end if

    # end _has_children

    is_wallet = fields.Boolean(string="Conto di portafoglio", default=is_wallet_default)

    wallet_ids = fields.One2many(
        comodel_name="account.journal",
        inverse_name="main_bank_account_id",
        string="Conti di portafoglio",
        default=_set_wallet_ids_default,
        readonly=True,
    )

    main_bank_account_id = fields.Many2one(
        comodel_name="account.journal",
        string="Conto principale di liquidità",
        domain= _domain_main_sezionale,
        default=_set_main_bank_account_id_default,
    )

    has_children = fields.Boolean(string="Conto padre", compute="_has_children")

    # ACCOUNTS

    invoice_financing_evaluate = fields.Selection(
        [
            ("invoice_amount", "percentuale su totale"),
            ("taxable_amount", "imponibile su imponibile"),
        ],
        string="Metodo calcolo anticipo fatture",
    )

    invoice_financing_percent = fields.Float(
        string="Percentuale di anticipo fatture",
        default=None,
    )

    sezionale = fields.Many2one(
        string="Sezionale",
        comodel_name="account.journal",
        domain=_domain_sezionale,
    )

    effetti_allo_sconto = fields.Many2one(
        string="Effetti allo sconto",
        comodel_name="account.account",
        domain=_domain_effetti_allo_sconto,
        help=(
            "Conto usato (in dare) per l'accredito distinta\n"
            "Per gestire il controllo del credito cliente\n"
            "usare un conto di tipo credito cliente"
        )
    )

    portafoglio_sbf = fields.Many2one(
        string="Conto portafoglio SBF",
        comodel_name="account.account",
        domain=_domain_portafoglio_sbf,
        help=(
            "Conto di portafoglio bancario SBF dopo accredito distinta\n"
            "Questo conto è la copia del conto di portafoglio del e-banking\n"
            "Non può esser usato in caso di uso effetti presentati\n"
        )
    )

    effetti_presentati = fields.Many2one(
        string="Effetti presentatti SBF",
        comodel_name="account.account",
        domain=_domain_effetti_presentati,
        help=(
            "Conto usato (in dare) per l'incasso cliente in 3 passi\n"
            "L'effetto transita per i conti attivo->sconto->presentato\n"
            "invece dell'usuale ciclo attivo->sconto\n"
            "Attenzione! Si perde il controllo del credito verso il cliente\n"
            "e non è possibile gestire la disponibilità del portafoglio!"
        )
    )

    default_bank_expenses_account = fields.Many2one(
        string="Conto di default per spese bancarie",
        comodel_name="account.account",
        domain=_domain_expenses_account,
        help="Conto predefinito per registrare le spese bancarie"
    )

    limite_effetti_sbf = fields.Float(string="Affidamento bancario SBF", default=0.0)

    importo_effetti_sbf = fields.Float(
        string="Portafoglio utilizzato", compute="_importo_effetti"
    )

    impegno_effetti_sbf = fields.Float(
        string="Importo da presentare", compute="_impegno_effetti"
    )

    disponibilita_effetti_sbf = fields.Float(
        string="Disponibilità residua", compute="_disponibilita_effetti"
    )

    @api.model
    def create(self, vals):
        result = super().create(vals)
        self._validate_invoice_financing_percent()
        return result

    @api.multi
    def write(self, vals):
        result = super().write(vals)
        for journal in self:
            journal._validate_invoice_financing_percent()
        return result

    @api.onchange("is_wallet")
    def _on_change_is_wallet(self):
        if not self.is_wallet:
            if self.main_bank_account_id:
                self.main_bank_account_id = self._set_main_bank_account_id_default()
        else:
            if (
                self.default_debit_account_id.user_type_id
                !=
                self.env.ref("account.data_account_type_receivable")
            ):
                return {
                    "warning": {
                        "title": _("Attenzione"),
                        "message": _(
                            "Il conto dare predefinito deve essere "
                            "un conto di tipo credito clienti"
                        ),
                    }
                }
            if (
                self.default_credit_account_id.user_type_id
                !=
                self.env.ref("account.data_account_type_receivable")
            ):
                return {
                    "warning": {
                        "title": _("Attenzione"),
                        "message": _(
                            "Il conto avere predefinito deve essere "
                            "un conto di tipo credito clienti"
                        ),
                    }
                }
        if self.bank_account_id:
            bank_account = self.env["res.partner.bank"].browse(self.bank_account_id.id)
            bank_account.write({"bank_is_wallet": self.is_wallet})

    @api.model
    def get_payment_method_config(self):
        return {
            "sezionale": self.sezionale,
            "transfer_journal": self.sezionale,
            "transfer_account": self.portafoglio_sbf,
            "banca_conto_effetti": self.portafoglio_sbf,
            "conto_effetti_attivi": self.portafoglio_sbf,
            "effetti_allo_sconto": self.effetti_allo_sconto,
            "conto_spese_bancarie": self.default_bank_expenses_account,
            "effetti_presentati": self.effetti_presentati,
        }

    @api.onchange("invoice_financing_evaluate")
    def _onchange_invoice_financing_evaluate(self):

        method = self.invoice_financing_evaluate
        pct_default = self._DEFAULT_FINANCING_PCT.get(method, 0)
        pct_set = bool(self.invoice_financing_percent)

        if not pct_set or not method:
            self.invoice_financing_percent = pct_default
        # end if

    # _onchange_invoice_financing_evaluate

    @api.model
    def _validate_invoice_financing_percent(self):

        ife_set = self.invoice_financing_evaluate is not False
        pct_set = self.invoice_financing_percent not in [False, 0]

        if ife_set and not pct_set:
            raise UserError(
                "Percentuale anticipo non impostata! "
                "La percentuale deve essere maggiore di zero"
            )
        # end if

    # end _validate_invoice_financing_percent
