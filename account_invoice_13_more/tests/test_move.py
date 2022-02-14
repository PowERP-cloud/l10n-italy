# -*- coding: utf-8 -*-
"""
Tests are based on test environment created by module mk_test_env of repository
https://github.com/zeroincombenze/zerobug-test

Each model must have a+one or mode dictionary; name should be TEST_model,
where model is the upercase model name with dot replaced by '_'
i.e.: res_partner -> TEST_RES_PARTNER

Every key of the model dictionary is the external reference with data dictionary
i.e.:
TEST_RES_PARTNER = {
    'z0bug.partner1': {
        'name': 'Alpha',
        'street': '1, First Avenue',
        ...
    }
}
The dictionary TEST_SETUP is the dictionary with data to load at setup.
TEST_SETUP = {
    'res.partner': TEST_RES_PARTNER,
    ...
}

In setup() function, the following code
    self.setup_records(lang='it_IT')
creates all record declared by above data; lang is optional parameter.

Final notes:
* Many2one value must be declared as external identifier
"""
from odoo.tests import common

TEST_ACCOUNT_ACCOUNT = {
    'external.3101': {
        'code': '3101',
        'name': 'merci c/vendite',
        'user_type_id': 'account.data_account_type_revenue',
        'reconcile': False
    },
    'external.4101': {
        'code': '4101',
        'name': 'merci c/acquisti',
        'user_type_id': 'account.data_account_type_expenses',
        'reconcile': False
    },
    'external.1601': {
        'code': '1601',
        'name': 'IVA n/credito',
        'user_type_id': 'account.data_account_type_current_assets',
        'reconcile': False
    },
    'external.2601': {
        'code': '2601',
        'name': 'IVA n/debito ',
        'user_type_id': 'account.data_account_type_current_liabilities',
        'reconcile': False
    },
}
TEST_ACCOUNT_TAX = {
    'by': 'description',
    'external.22v': {
        'description': '22v',
        'name': 'IVA 22%',
        'amount': 22,
        'amount_type': 'percent',
        'type_tax_use': 'sale',
        'account_id': 'external.1601',
        'refund_account_id': 'external.1601',
    },
    'external.22a': {
        'description': '22a',
        'name': 'IVA 22%',
        'amount': 22,
        'amount_type': 'percent',
        'type_tax_use': 'purchase',
        'account_id': 'external.1601',
        'refund_account_id': 'external.1601',
    },
}
TEST_ACCOUNT_PAYMENT_TERM = {
    'z0bug.payment_1': {
        'name': 'RiBA 30GG/FM',
        'riba': True,
        'riba_payment_cost': 2.5,
    }
}
TEST_ACCOUNT_FISCAL_POSITION = {
    'z0bug.fiscalpos_it': {
        'name': 'Italia',
    },
}
TEST_RES_PARTNER = {
    'z0bug.res_partner_1': {
        'name': 'Prima Alpha S.p.A.',
        'street': 'Via I Maggio, 101',
        'country_id': 'base.it',
        'zip': '20022',
        'city': 'Castano Primo',
        'state_id': 'base.state_it_mi',
        'customer': True,
        'supplier': True,
        'is_company': True,
        'email': 'info@prima-alpha.it',
        'phone': '+39 0255582285',
        'vat': 'IT00115719999',
        'website': 'http://www.prima-alpha.it',
        'property_account_position_id': 'z0bug.fiscalpos_it',
        'property_payment_term_id': 'z0bug.payment_1',
        'property_supplier_payment_term_id': 'z0bug.payment_1',
        'electronic_invoice_subjected': 1,
        'codice_destinatario': 'A1B2C3X',
        'lang': 'it_IT',
    },
}
TEST_RES_PARTNER_BANK = {
    'z0bug.bank_company_1': {
        'acc_number': 'IT15A0123412345100000123456',
        'partner_id': 'base.main_partner',
        'acc_type': 'iban',
    },
}
TEST_PRODUCT_TEMPLATE = {
    'by': 'default_code',
    'z0bug.product_template_1': {
        'default_code': 'AA',
        'name': 'Prodotto Alpha',
        'lst_price': 0.84,
        'standard_price': 0.42,
        'type': 'consu',
        'taxes_id': 'external.22v',
        'supplier_taxes_id': 'external.22a',
        'property_account_income_id': 'external.3101',
        'property_account_expense_id': 'external.4101',
    },
}
TEST_SETUP = {
    'account.account': TEST_ACCOUNT_ACCOUNT,
    'account.tax': TEST_ACCOUNT_TAX,
    'account.payment.term': TEST_ACCOUNT_PAYMENT_TERM,
    'account.fiscal.position': TEST_ACCOUNT_FISCAL_POSITION,
    'res.partner': TEST_RES_PARTNER,
    'res.partner.bank': TEST_RES_PARTNER_BANK,
    'product.template': TEST_PRODUCT_TEMPLATE,
}

TEST_ACCOUNT_INVOICE_LINE = {
    '1': {
        # 'invoice_id': 'z0bug.invoice_Z0_1',
        'product_id': 'z0bug.product_product_1',
        'name': 'Prodotto Alpha',
        'quantity': 1,
        'price_unit': 0.84,
        'account_id': 'external.3101',
        'invoice_line_tax_ids': 'external.22v',
    },
}
TEST_ACCOUNT_INVOICE = {
    'z0bug.invoice_Z0_1': {
        'partner_id': 'z0bug.res_partner_1',
        'origin': 'P1/2021/0001',
        'reference': 'P1/2021/0001',
        'type': 'out_invoice',                                  # Field to test
        'journal_id': 'external.INV',
        'fiscal_position_id': 'z0bug.fiscalpos_it',             # Field to test
        'payment_term_id': 'z0bug.payment_1',                   # Field to test
        'partner_bank_id': 'z0bug.bank_company_1',              # Field to test
        'date_invoice': '2022-01-01',                           # Field to test
    },
}


class TestAccountMove(common.TransactionCase):

    # --------------------------------------- #
    # Common code: may be share among modules #
    # --------------------------------------- #

    def simulate_xref(self, xref, raise_if_not_found=None,
                      model=None, by=None, company_id=None, case=None):
        """Simulate External Reference
        This function simulates self.env.ref() searching for model record.
        Ordinary xref is formatted as "MODULE.NAME"; when MODULE = "external"
        this function is executed.
        Record is searched by <by> parameter, default is 'code' or 'name';
        id NAME is formatted as "FIELD=VALUE", FIELD value is assigned to <by>
        If company_id is supplied, it is added in search domain;

        Args:
            xref (str): external reference
            raise_if_not_found (bool): raise exception if xref not found or
                                       if more records found
            model (str): external reference model
            by (str): default field to search object record,
            company_id (int): company ID
            case: apply for uppercase or lowercase

        Returns:
            obj: the model record
        """
        if model not in self.env:
            if raise_if_not_found:
                raise ValueError('Model %s not found in the system' % model)
            return False
        _fields = self.env[model].fields_get()
        if not by:
            if model in self.by:
                by = self.by[model]
            else:
                by = 'code' if 'code' in _fields else 'name'
        module, name = xref.split('.', 1)
        if '=' in name:
            by, name = name.split('=', 1)
        if case == 'upper':
            name = name.upper()
        elif case == 'lower':
            name = name.lower()
        domain = [(by, '=', name)]
        if company_id and 'company_id' in _fields:
            domain.append(('company_id', '=', company_id))
        objs = self.env[model].search(domain)
        if len(objs) == 1:
            return objs[0]
        if raise_if_not_found:
            raise ValueError('External ID not found in the system: %s' % xref)
        return False

    def env_ref(self, xref, raise_if_not_found=None,
                model=None, by=None, company_id=None, case=None):
        """Get External Reference
        This function is like self.env.ref(); if xref does not exist and
        xref prefix is 'external.', engage simulate_xref

        Args:
            xref (str): external reference, format is "module.name"
            raise_if_not_found (bool): raise exception if xref not found
            model (str): external ref. model; required for "external." prefix
            by (str): field to search object record, default is 'code' or 'name'
            company_id (int): company ID

        Returns:
            obj: the model record
        """
        if xref is False or xref is None:
            return xref
        obj = self.env.ref(xref, raise_if_not_found=raise_if_not_found)
        if not obj:
            module, name = xref.split('.', 1)
            if module == 'external':
                return self.simulate_xref(xref,
                                          model=model,
                                          by=by,
                                          company_id=company_id,
                                          case=case)
        return obj

    def add_xref(self, xref, model, xid):
        """Add external reference to use in next tests.
        If xref exist, result ID will be upgraded"""
        module, name = xref.split('.', 1)
        if module == 'external':
            return False
        ir_model = self.env['ir.model.data']
        vals = {
            'module': module,
            'name': name,
            'model': model,
            'res_id': xid,
        }
        xrefs = ir_model.search([('module', '=', module),
                                 ('name', '=', name)])
        if not xrefs:
            return ir_model.create(vals)
        xrefs[0].write(vals)
        return xrefs[0]

    def get_values(self, model, values, by=None, company_id=None, case=None):
        """Load data values and set them in dictionary to create
        * Not existents fields are ignored
        * Many2one field are filled with current record ID
        """
        _fields = self.env[model].fields_get()
        vals = {}
        for item in values.keys():
            if item not in _fields:
                continue
            if item == 'company_id' and not values[item]:
                vals[item] = company_id
            elif _fields[item]['type'] == 'many2one':
                res = self.env_ref(
                    values[item],
                    model=_fields[item]['relation'],
                    by=by,
                    company_id=company_id,
                    case=case,
                )
                vals[item] = res.id if res else res
            elif (_fields[item]['type'] == 'many2many' and
                  '.' in values[item] and
                  ' ' not in values[item]):
                res = self.env_ref(
                    values[item],
                    model=_fields[item]['relation'],
                    by=by,
                    company_id=company_id,
                    case=case,
                )
                vals[item] = [(6, 0, [res.id])] if res else res
            else:
                vals[item] = values[item]
        return vals

    def model_create(self, model, values, xref=None):
        """Create a test record and set external ID to next tests"""
        res = self.env[model].create(values)
        if xref and ' ' not in xref:
            self.add_xref(xref, model, res.id)
        return res

    def model_browse(self, model, xid):
        """Browse a record by external ID"""
        res_id = self.ref(xid) if isinstance(xid, str) else xid
        return self.env[model].browse(res_id)

    def model_make(self, model, values, xref):
        """Create or write a test record and set external ID to next tests"""
        res_id = self.env_ref(xref, model=model)
        if res_id:
            recs = self.env[model].search([('id', '=', res_id)])
            if recs:
                rec = recs[0]
                rec.write(values)
                return rec
        return self.model_create(model, values, xref=xref)

    def default_company(self):
        return self.env.user.company_id

    def set_locale(self, locale_name, raise_if_not_found=True):
        modules_model = self.env['ir.module.module']
        modules = modules_model.search([('name', '=', locale_name)])
        if modules and modules[0].state != 'uninstalled':
            modules = []
        if modules:
            modules.button_immediate_install()
            self.env['account.chart.template'].try_loading_for_current_company(
                locale_name
            )
        else:
            if raise_if_not_found:
                raise ValueError(
                    'Module %s not found in the system' % locale_name)

    def install_language(self, iso, overwrite=None, force_translation=None):
        iso = iso or 'en_US'
        overwrite = overwrite or False
        load = False
        lang_model = self.env['res.lang']
        languages = lang_model.search([('code', '=', iso)])
        if not languages:
            languages = lang_model.search([('code', '=', iso),
                                           ('active', '=', False)])
            if languages:
                languages.write({'active': True})
                load = True
        if not languages or load:
            vals = {
                'lang': iso,
                'overwrite': overwrite,
            }
            self.env['base.language.install'].create(vals).lang_install()
        if force_translation:
            vals = {'lang': iso}
            self.env['base.update.translations'].create(vals).act_update()

    def setup_records(self, lang=None, locale=None, company=None):
        """Create all record from declared data. See above doc"""

        def iter_data(model, model_data, company):
            for item in model_data.keys():
                if isinstance(model_data[item], str):
                    continue
                vals = self.get_values(
                    model,
                    model_data[item],
                    company_id=company.id)
                res = self.model_make(model, vals, item)
                if model == 'product.template':
                    model2 = 'product.product'
                    vals = self.get_values(
                        model2,
                        model_data[item],
                        company_id=company.id)
                    vals['product_tmpl_id'] = res.id
                    self.model_make(
                        model2, vals, item.replace('template', 'product'))

        if locale:
            self.set_locale(locale)
        if lang:
            self.install_language('it_IT')
        self.by = {}
        for model, model_data in TEST_SETUP.items():
            by = model_data.get('by')
            if by:
                self.by[model] = by
        company = company or self.default_company()
        for model, model_data in TEST_SETUP.items():
            by = model_data.get('by')
            iter_data(model, model_data, company)

    # ------------------ #
    # Specific test code #
    # ------------------ #
    def setUp(self):
        super().setUp()
        self.setup_records(lang='it_IT')

    def test_invoice_validate(self):
        for item in TEST_ACCOUNT_INVOICE:
            model = 'account.invoice'
            vals = self.get_values(
                model,
                TEST_ACCOUNT_INVOICE[item])
            inv = self.model_make(model, vals, item)

            model = 'account.invoice.line'
            for line in TEST_ACCOUNT_INVOICE_LINE.values():
                vals = self.get_values(model, line)
                vals['invoice_id'] = inv.id
                self.model_make(model, vals, False)
            inv.compute_taxes()
            inv.action_invoice_open()
            move = inv.move_id
            for field in ('type',
                          'payment_term_id',
                          'fiscal_position_id',
                          'partner_bank_id'):
                self.assertEqual(getattr(inv, field), getattr(move, field))
            self.assertEqual(getattr(inv, 'date_invoice'),
                             getattr(move, 'invoice_date'))
