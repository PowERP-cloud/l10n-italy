"""
Tests are based on test environment created by module mk_test_env in repository
https://github.com/zeroincombenze/zerobug-test

Each model is declared by a dictionary which name should be "TEST_model",
where model is the uppercase model name with dot replaced by "_".
i.e.: res_partner -> TEST_RES_PARTNER

Every record is declared in the model dictionary by a key which is the external
reference used to retrieve the record.
i.e. the following record is named 'z0bug.partner1':
TEST_RES_PARTNER = {
    "z0bug.partner1": {
        "name": "Alpha",
        "street": "1, First Avenue",
        ...
    }
}

The magic dictionary TEST_SETUP contains data to load at test setup.
TEST_SETUP = {
    "res.partner": TEST_RES_PARTNER,
    ...
}

In setup() function, the following code
    self.setup_records(lang="it_IT")
creates all record declared by above data; lang is an optional parameter.

Final notes:
* Many2one value must be declared as external identifier
* Written on 2022-11-16 11:18:07.934593 by mk_test_env 12.0.0.7.6
"""
import os
import logging
# from odoo.tests import common
from .envtest import EnvTest as SingleTransactionCase

_logger = logging.getLogger(__name__)

# Record data for base models
TEST_ACCOUNT_ACCOUNT = {
    "external.2601": {
        "code": "2601",
        "name": "IVA n/debito",
        "user_type_id": "account.data_account_type_current_liabilities",
        "reconcile": False,
    },
    "external.3112": {
        "code": "3112",
        "name": "Ricavi da merci e servizi",
        "user_type_id": "account.data_account_type_revenue",
        "reconcile": False,
    },
    "external.3101": {
        "code": "3101",
        "name": "Merci c/vendita",
        "user_type_id": "account.data_account_type_revenue",
        "reconcile": False,
    },
}
TEST_ACCOUNT_FISCAL_POSITION = {
    "z0bug.fiscalpos_it": {
        "name": "Italia",
    },
}
TEST_ACCOUNT_JOURNAL = {
    "external.INV": {
        "name": "Fatture di vendita",
        "code": "INV",
        "type": "sale",
        "update_posted": True,
    },
    "z0bug.bank11_journal": {
        "name": "B. Pop. Software (IT15*456)",
        "bank_account_id": "z0bug.bank_company_1",
        "code": "BNK11",
        "type": "bank",
        "sequence": 10,
        # "default_debit_account_id": "z0bug.coa_180003",
        # "default_credit_account_id": "z0bug.coa_180003",
        "update_posted": True,
        # "default_bank_expenses_account": "z0bug.coa_731140",
    },
    "z0bug.bank13_journal": {
        "name": "Portafoglio RiBA e SDD – B. Pop. Soft. (IT15*456)",
        "bank_account_id": "z0bug.bank_company_1a",
        "code": "BNK13",
        "type": "bank",
        "sequence": 20,
        # "default_debit_account_id": "z0bug.coa_152210",
        # "default_credit_account_id": "z0bug.coa_152210",
        "is_wallet": True,
        "main_bank_account_id": "z0bug.bank11_journal",
        "update_posted": True,
        # "default_bank_expenses_account": "z0bug.coa_731140",
        "sezionale": "z0bug.bank11_journal",
        "limite_effetti_sbf": 5000,
    },
}
TEST_PAYMENT_METHOD = {
    "account_banking_riba.riba": {
        "code": "riba_cbi",
        "name": "RIBA CBI",
        "payment_type": "inbound",
    }
}
TEST_PAYMENT_MODE = {
    "z0bug.pmode_riba": {
        "name": "RiBA SBF",
        "bank_account_link": "variable",
        "type": "sale",
        "payment_method_id": "account_banking_riba.riba",
        "payment_type": "inbound",
    },
}
TEST_ACCOUNT_PAYMENT_TERM = {
    "z0bug.payment_1": {
        "name": "RiBA 30GG/FM",
        "fatturapa_pt_id": "l10n_it_fiscal_payment_term.fatturapa_tp02",
        "fatturapa_pm_id": "l10n_it_fiscal_payment_term.fatturapa_mp12",
    },
    "z0bug.payment_2": {
        "name": "RiBA 30/60 GG/FM",
        "fatturapa_pt_id": "l10n_it_fiscal_payment_term.fatturapa_tp01",
        "fatturapa_pm_id": "l10n_it_fiscal_payment_term.fatturapa_mp12",
    },
}
TEST_ACCOUNT_PAYMENT_TERM_LINE = {
    "parent": "payment_id",
    "by": "sequence",
    "z0bug.payment_1_9": {
        "payment_id": "z0bug.payment_1",
        "sequence": 9,
        "days": 28,
        "value": "balance",
        "option": "after_invoice_month",
        "payment_method_credit": "account_banking_riba.riba",
    },
    "z0bug.payment_2_1": {
        "payment_id": "z0bug.payment_2",
        "sequence": 1,
        "days": 28,
        "value": "percent",
        "value_amount": 50,
        "option": "after_invoice_month",
        "payment_method_credit": "account_banking_riba.riba",
    },
    "z0bug.payment_2_9": {
        "payment_id": "z0bug.payment_2",
        "sequence": 9,
        "days": 58,
        "value": "balance",
        "option": "after_invoice_month",
        "payment_method_credit": "account_banking_riba.riba",
    },
}

TEST_ACCOUNT_TAX = {
    "by": "description",
    "external.22v": {
        "description": "22v",
        "name": "IVA 22% su vendite",
        "amount": 22,
        "amount_type": "percent",
        "type_tax_use": "sale",
        "price_include": False,
        "account_id": "external.2601",
        "refund_account_id": "external.2601",
    },
}
TEST_RES_PARTNER = {
    "z0bug.res_partner_1": {
        "name": "Prima Alpha S.p.A.",
        "street": "Via I Maggio, 101",
        "country_id": "base.it",
        "zip": "20022",
        "city": "Castano Primo",
        "state_id": "base.state_it_mi",
        "customer": True,
        "supplier": True,
        "is_company": True,
        "email": "info@prima-alpha.it",
        "phone": "+39 0255582285",
        "vat": "IT00115719999",
        "website": "http://www.prima-alpha.it",
        "property_account_position_id": "z0bug.fiscalpos_it",
        "property_payment_term_id": "z0bug.payment_1",
        "property_supplier_payment_term_id": "z0bug.payment_1",
        "electronic_invoice_subjected": True,
        "codice_destinatario": "A1B2C3X",
        "lang": "it_IT",
    },
    "z0bug.res_partner_2": {
        "name": "Latte Beta Due s.n.c.",
        "street": "Via Dueville, 2",
        "country_id": "base.it",
        "zip": "10060",
        "city": "S. Secondo Pinerolo",
        "state_id": "base.state_it_to",
        "customer": True,
        "supplier": False,
        "is_company": True,
        "email": "agrolait2@libero.it",
        "phone": "+39 0121555123",
        "vat": "IT02345670018",
        "website": "http://www.agrolait2.it/",
        "property_account_position_id": "z0bug.fiscalpos_it",
        "property_payment_term_id": "z0bug.payment_2",
        "electronic_invoice_subjected": True,
        "codice_destinatario": "ABCDEFG",
        "goods_description_id": "l10n_it_ddt.goods_description_SFU",
        "carriage_condition_id": "l10n_it_ddt.carriage_condition_PAF",
        "transportation_method_id": "l10n_it_ddt.transportation_method_COR",
        "lang": "it_IT",
    },
}
TEST_RES_PARTNER_BANK = {
    "z0bug.bank_company_1": {
        "acc_number": "IT15A0123412345100000123456",
        "partner_id": "base.main_partner",
        "acc_type": "iban",
        "bank_id": "z0bug.bank_bps",
    },
    "z0bug.bank_company_1a": {
        "acc_number": "Portafoglio RiBA",
        "partner_id": "base.main_partner",
        "acc_type": "bank",
        "bank_is_wallet": True,
        "bank_main_bank_account_id": "z0bug.bank_company_1",
    },
    "z0bug.bank_partner_1": {
        "acc_number": "IT73C0102001011010101987654",
        "partner_id": "z0bug.res_partner_1",
        "acc_type": "iban",
    },
    "z0bug.bank_partner_2": {
        "acc_number": "IT82B0200802002200000000022",
        "partner_id": "z0bug.res_partner_2",
        "acc_type": "iban",
        "bank_id": "z0bug.bank_unicr",
    },
}
TEST_ACCOUNT_INVOICE_LINE = {
    "z0bug.invoice_Z0_1_01": {
        "invoice_id": "z0bug.invoice_Z0_1",
        "product_id": "z0bug.product_product_1",
        "name": "Prodotto Alpha",
        "quantity": 100,
        "account_id": "external.3112",
        "price_unit": 0.84,
        "invoice_line_tax_ids": "external.22v",
    },
    "z0bug.invoice_Z0_1_02": {
        "invoice_id": "z0bug.invoice_Z0_1",
        "product_id": "z0bug.product_product_2",
        "name": "Prodotto Beta",
        "quantity": 200,
        "account_id": "external.3112",
        "price_unit": 3.38,
        "invoice_line_tax_ids": "external.22v",
    },
    "z0bug.invoice_Z0_2_1": {
        "invoice_id": "z0bug.invoice_Z0_2",
        "product_id": "z0bug.product_product_1",
        "name": "Prodotto Alpha",
        "quantity": 100,
        "account_id": "external.3101",
        "price_unit": 0.42,
        "invoice_line_tax_ids": "external.22v",
    },
    "z0bug.invoice_Z0_2_2": {
        "invoice_id": "z0bug.invoice_Z0_2",
        "product_id": "z0bug.product_product_2",
        "name": "Prodotto Beta",
        "quantity": 100,
        "account_id": "external.3101",
        "price_unit": 1.69,
        "invoice_line_tax_ids": "external.22v",
    },
}

# Record data for models to test
TEST_ACCOUNT_INVOICE = {
    "z0bug.invoice_Z0_1": {
        "partner_id": "z0bug.res_partner_1",
        "origin": "P1/2021/0001",
        "reference": "P1/2021/0001",
        "date_invoice": "2022-10-31",
        "type": "out_invoice",
        "journal_id": "external.INV",
        "fiscal_position_id": "z0bug.fiscalpos_it",
        "partner_bank_id": "z0bug.bank_company_1",
        "payment_term_id": "z0bug.payment_1",
        "company_bank_id": "z0bug.bank_company_1",
        "counterparty_bank_id": "z0bug.bank_partner_1",
    },
    "z0bug.invoice_Z0_2": {
        "partner_id": "z0bug.res_partner_2",
        "origin": "SO123",
        "reference": "SO123",
        "date_invoice": "2022-10-31",
        "type": "out_invoice",
        "journal_id": "external.INV",
        "fiscal_position_id": "z0bug.fiscalpos_it",
        "partner_bank_id": "z0bug.bank_company_1",
        "payment_term_id": "z0bug.payment_2",
        "company_bank_id": "z0bug.bank_company_1",
        "counterparty_bank_id": "z0bug.bank_partner_2",
    },
}
TEST_SETUP_LIST = [
    "account.account",
    "account.fiscal.position",
    "account.payment.method",
    "account.payment.mode",
    "account.payment.term",
    "account.payment.term.line",
    "res.partner",
    "res.partner.bank",
    "account.tax",
    "account.journal",
    "account.invoice",
    "account.invoice.line",
]
TEST_SETUP = {
    "account.account": TEST_ACCOUNT_ACCOUNT,
    "account.fiscal.position": TEST_ACCOUNT_FISCAL_POSITION,
    "account.journal": TEST_ACCOUNT_JOURNAL,
    "account.payment.method": TEST_PAYMENT_METHOD,
    "account.payment.mode": TEST_PAYMENT_MODE,
    "account.payment.term": TEST_ACCOUNT_PAYMENT_TERM,
    "account.payment.term.line": TEST_ACCOUNT_PAYMENT_TERM_LINE,
    "account.tax": TEST_ACCOUNT_TAX,
    "res.partner": TEST_RES_PARTNER,
    "res.partner.bank": TEST_RES_PARTNER_BANK,
    "account.invoice": TEST_ACCOUNT_INVOICE,
    "account.invoice.line": TEST_ACCOUNT_INVOICE_LINE,
}

# Record data for child models
TEST_ACCOUNT_PAYMENT_LINE = {
    # "external.pay_order_1_1": {
    #     "order_id": "external.pay_order_1",
    # }
}
TEST_ACCOUNT_PAYMENT_ORDER = {
    "external.pay_order_1": {
        "payment_mode_id": "z0bug.pmode_riba",
        "date_prefered": "due",
        "journal_id": "z0bug.bank13_journal",
    }
}
TNL_RECORDS = {
    "product.product": {
        # "type": ["product", "consu"],
    },
    "product.template": {
        # "type": ["product", "consu"],
    },
}


class AccountInvoice(SingleTransactionCase):

    # --------------------------------------- #
    # Common code: may be share among modules #
    # --------------------------------------- #

    def simulate_xref(
        self,
        xref,
        raise_if_not_found=None,
        model=None,
        by=None,
        company=None,
        case=None,
    ):
        """Simulate External Reference
        This function simulates self.env.ref() searching for model record.
        Ordinary xref is formatted as "MODULE.NAME"; when MODULE = "external"
        this function is called.
        Record is searched by <by> parameter, default is "code" or "name";
        id NAME is formatted as "FIELD=VALUE", FIELD value is assigned to <by>
        If company is supplied, it is added in search domain;

        Args:
            xref (str): external reference
            raise_if_not_found (bool): raise exception if xref not found or
                                       if more records found
            model (str): external reference model
            by (str): default field to search object record,
            company (obj): default company
            case: apply for uppercase or lowercase

        Returns:
            obj: the model record
        """
        if model not in self.env:
            if raise_if_not_found:
                raise ValueError("Model %s not found in the system" % model)
            return False
        _fields = self.env[model].fields_get()
        if not by:
            if model in self.by:
                by = self.by[model]
            else:
                by = "code" if "code" in _fields else "name"
        module, name = xref.split(".", 1)
        if "=" in name:
            by, name = name.split("=", 1)
        if case == "upper":
            name = name.upper()
        elif case == "lower":
            name = name.lower()
        parent = self.parent.get(model)
        if parent:
            x = name.split("_")
            name = "_".join(x[:-1])
            x = x[-1]
            if x.isdigit():
                x = eval(x)
            domain = [(by, "=", x)]
            domain.append((parent, "=", self.env_ref("%s.%s" % (module, name)).id))
        else:
            domain = [(by, "=", name)]
        if (
            model
            not in ("product.product", "product.template", "res.partner", "res.users")
            and company
            and "company_id" in _fields
        ):
            domain.append(("company_id", "=", company.id))
        objs = self.env[model].search(domain)
        if len(objs) == 1:
            return objs[0]
        if raise_if_not_found:
            raise ValueError("External ID not found in the system: %s" % xref)
        return False

    def env_ref(
        self,
        xref,
        raise_if_not_found=None,
        model=None,
        by=None,
        company=None,
        case=None,
    ):
        """Get External Reference
        This function is like self.env.ref(); if xref does not exist and
        xref prefix is "external.", engage simulate_xref

        Args:
            xref (str): external reference, format is "module.name"
            raise_if_not_found (bool): raise exception if xref not found
            model (str): external ref. model; required for "external." prefix
            by (str): field to search for object record (def "code" or "name")
            company (obj): default company

        Returns:
            obj: the model record
        """
        if xref is False or xref is None:
            return xref
        obj = self.env.ref(xref, raise_if_not_found=raise_if_not_found)
        if not obj:
            module, name = xref.split(".", 1)
            if module == "external" or self.parent.get(model):
                return self.simulate_xref(
                    xref, model=model, by=by, company=company, case=case
                )
        return obj

    def add_xref(self, xref, model, xid):
        """Add external reference that will be used in next tests.
        If xref exist, result ID will be upgraded"""
        module, name = xref.split(".", 1)
        if module == "external":
            return False
        ir_model = self.env["ir.model.data"]
        vals = {
            "module": module,
            "name": name,
            "model": model,
            "res_id": xid,
        }
        xrefs = ir_model.search([("module", "=", module), ("name", "=", name)])
        if not xrefs:
            return ir_model.create(vals)
        xrefs[0].write(vals)
        return xrefs[0]

    def get_values(self, model, values, by=None, company=None, case=None):
        """Load data values and set them in a dictionary for create function
        * Not existent fields are ignored
        * Many2one field are filled with current record ID
        """
        _fields = self.env[model].fields_get()
        vals = {}
        if model in TNL_RECORDS:
            for item in TNL_RECORDS[model].keys():
                if item in values:
                    (old, new) = TNL_RECORDS[model][item]
                    if values[item] == old:
                        values[item] = new
        for item in values.keys():
            if item not in _fields:
                continue
            if item == "company_id" and not values[item]:
                vals[item] = company.id
            elif _fields[item]["type"] == "many2one":
                res = self.env_ref(
                    values[item],
                    model=_fields[item]["relation"],
                    by=by,
                    company=company,
                    case=case,
                )
                if res:
                    vals[item] = res.id
            elif (
                _fields[item]["type"] == "many2many"
                and "." in values[item]
                and " " not in values[item]
            ):
                res = self.env_ref(
                    values[item],
                    model=_fields[item]["relation"],
                    by=by,
                    company=company,
                    case=case,
                )
                if res:
                    vals[item] = [(6, 0, [res.id])]
            elif values[item] is not None:
                vals[item] = values[item]
        return vals

    def model_create(self, model, values, xref=None):
        """Create a test record and set external ID to next tests"""
        if model.startswith("account.move"):
            res = self.env[model].with_context(check_move_validity=False).create(values)
        else:
            res = self.env[model].create(values)
        if xref and " " not in xref:
            self.add_xref(xref, model, res.id)
        return res

    def model_browse(self, model, xid, company=None, by=None, raise_if_not_found=True):
        """Browse a record by external ID"""
        res = self.env_ref(
            xid,
            model=model,
            company=company,
            by=by,
        )
        if res:
            return res
        return self.env[model]

    def model_make(self, model, values, xref, company=None, by=None):
        """Create or write a test record and set external ID to next tests"""
        res = self.model_browse(
            model, xref, company=company, by=by, raise_if_not_found=False
        )
        if res:
            if model.startswith("account.move"):
                res.with_context(check_move_validity=False).write(values)
            else:
                res.write(values)
            return res
        return self.model_create(model, values, xref=xref)

    def default_company(self):
        return self.env.user.company_id

    def set_locale(self, locale_name, raise_if_not_found=True):
        modules_model = self.env["ir.module.module"]
        modules = modules_model.search([("name", "=", locale_name)])
        if modules and modules[0].state != "uninstalled":
            modules = []
        if modules:
            modules.button_immediate_install()
            self.env["account.chart.template"].try_loading_for_current_company(
                locale_name
            )
        else:
            if raise_if_not_found:
                raise ValueError("Module %s not found in the system" % locale_name)

    def install_language(self, iso, overwrite=None, force_translation=None):
        iso = iso or "en_US"
        overwrite = overwrite or False
        load = False
        lang_model = self.env["res.lang"]
        languages = lang_model.search([("code", "=", iso)])
        if not languages:
            languages = lang_model.search([("code", "=", iso), ("active", "=", False)])
            if languages:
                languages.write({"active": True})
                load = True
        if not languages or load:
            vals = {
                "lang": iso,
                "overwrite": overwrite,
            }
            self.env["base.language.install"].create(vals).lang_install()
        if force_translation:
            vals = {"lang": iso}
            self.env["base.update.translations"].create(vals).act_update()

    def setup_records(self, lang=None, locale=None, company=None, save_as_demo=None):
        """Create all record from declared data. See above doc

        Args:
            lang (str): install & load specific language
            locale (str): install locale module with CoA; i.e l10n_it
            company (obj): declare default company for tests
            save_as_demo (bool): commit all test data as they are demo data
            Warning: usa save_as_demo carefully; is used in multiple tests,
            like in travis this option can be cause to failue of tests
            This option can be used in local tests with "run_odoo_debug -T"

        Returns:
            None
        """

        def iter_data(model, model_data, company):
            for item in model_data.keys():
                if isinstance(model_data[item], str):
                    continue
                vals = self.get_values(model, model_data[item], company=company)
                res = self.model_make(model, vals, item, company=company)
                if model == "product.template":
                    model2 = "product.product"
                    vals = self.get_values(model2, model_data[item], company=company)
                    vals["product_tmpl_id"] = res.id
                    self.model_make(
                        model2,
                        vals,
                        item.replace("template", "product"),
                        company=company,
                    )

        self.save_as_demo = save_as_demo or False
        if locale:
            self.set_locale(locale)
        if lang:
            self.install_language(lang)
        if not self.env["ir.module.module"].search(
            [("name", "=", "stock"), ("state", "=", "installed")]
        ):
            TNL_RECORDS["product.product"]["type"] = ["product", "consu"]
            TNL_RECORDS["product.template"]["type"] = ["product", "consu"]
        company = company or self.default_company()
        self.by = {}
        self.parent = {}
        for model, model_data in TEST_SETUP.items():
            by = model_data.get("by")
            if by:
                self.by[model] = by
            parent = model_data.get("parent")
            if parent:
                self.parent[model] = parent
        for model in TEST_SETUP_LIST:
            model_data = TEST_SETUP[model]
            iter_data(model, model_data, company)

    # ------------------ #
    # Specific test code #
    # ------------------ #
    def setUp(self):
        super().setUp()
        self.setup_records(lang="it_IT")
        self.company = self.default_company()
        self.company.vat = "IT05111810015"
        self.company.sia_code = "A7721"
        pay_mode = self.env_ref("z0bug.pmode_riba")
        pay_mode.fixed_journal_id = self.env_ref("z0bug.bank13_journal")
        pay_mode.bank_account_link = "fixed"

    def tearDown(self):
        super().tearDown()
        if os.environ.get("ODOO_COMMIT_TEST", ""):
            self.env.cr.commit()  # pylint: disable=invalid-commit
            _logger.info("✨ Test data committed")

    def test_payment_order(self):
        for xref in TEST_ACCOUNT_INVOICE.keys():
            invoice = self.env_ref(xref)
            invoice.compute_taxes()
            invoice.action_invoice_open()
        # model = "account.payment.order"
        # model_child = "account.payment.line"
        # partners = (
        #     self.env_ref("z0bug.res_partner_1").id,
        #     self.env_ref("z0bug.res_partner_2").id,
        # )
        # xref = list(TEST_ACCOUNT_PAYMENT_ORDER.keys())[0]
        # _logger.info(
        #     "🎺 Testing %s[%s]" % (model, xref)
        # )
        # vals = self.get_values(
        #     model,
        #     TEST_ACCOUNT_PAYMENT_ORDER[xref])
        # pay_order = self.model_make(model, vals, xref)
        #
        # for due_record in self.env["account.move.line"].search(
        #     [
        #         ("user_type_id",
        #          "=",
        #          self.env.ref("account.data_account_type_receivable").id),
        #         ("journal_id.type", "=", "sale"),
        #         ("partner_id", "in", partners)
        #     ]
        # ):
        #     vals = {
        #         "order_id": pay_order.id,
        #         "move_line_id": due_record.id,
        #         "partner_id": due_record.partner_id.id,
        #         "communication": due_record.ref,
        #         "amount_currency": due_record.debit,
        #         "partner_bank_id": due_record.partner_id.bank_ids[0].id,
        #     }
        #     self.env[model_child].create(vals)
        #     # TODO> to remove early after banking common upgrade
        #     due_record.payment_order = pay_order
        #     due_record.payment_mode_id = self.env_ref("z0bug.pmode_riba")
        #     due_record.partner_bank_id = due_record.partner_id.bank_ids[0]
        partners = (
            self.env_ref("z0bug.res_partner_1").id,
            self.env_ref("z0bug.res_partner_2").id,
        )
        move_lines = self.env["account.move.line"].search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_receivable").id,
                ),
                ("journal_id.type", "=", "sale"),
                ("partner_id", "in", partners),
            ]
        )
        # self.wizard(
        #     module="account_banking_common",
        #     action_name="server_action_payment_order_generate",
        #     records=move_lines,
        # )

        # pay_order.draft2open()
        # self.assertEqual(
        #     pay_order.state,
        #     "open",
        #     "Payment order not opened!"
        # )
        # pay_order.open2generated()
        # self.assertEqual(
        #     pay_order.state,
        #     "generated",
        #     "Payment order not generated!"
        # )
        # pay_order.generated2uploaded()
        # self.assertEqual(
        #     pay_order.state,
        #     "uploaded",
        #     "Payment order not uploaded!"
        # )
